from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import CustomUser
from api.serializers import DormitoryAddressSerializer, BuildingSerializer, FloorSerializer, \
    FloorRoomsWithBuildingAndDormitorySerializer
from apps.e_manzil.models import DormitoryAddress, Building, Floor

# Yotoqxona manzillari ro'yxatini olish va qo'shish
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class DormitoryAddressList(generics.ListCreateAPIView):
    queryset = DormitoryAddress.objects.all()
    serializer_class = DormitoryAddressSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

# TTJ BINOLAR qo'shish
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_dormitory_address(request):
    serializer = DormitoryAddressSerializer(data=request.data)
    if serializer.is_valid():
        dormitory_address = serializer.save(created_by=request.user, updated_by=request.user)
        return Response({
            'status': 'success',
            'message': 'Record added successfully!',
            'data': DormitoryAddressSerializer(dormitory_address).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# TTJ Binolarni o'chirish
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
@method_decorator(require_http_methods(["DELETE"]), name='dispatch')
class DormitoryAddressDeleteView(View):
    def delete(self, request, *args, **kwargs):
        # Foydalanuvchini autentifikatsiya qilinganligini tekshirish
        if not request.user.is_authenticated:
            return HttpResponseForbidden('You do not have permission to perform this action.')

        # Yotoqxona manzilini olish
        address = get_object_or_404(DormitoryAddress, id=kwargs.get('id'))

        # Yotoqxona manziliga bog'langan binolarni tekshirish
        if address.buildings.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Bu yotoqxona manziliga bog‘langan binolar mavjud, o‘chira olmaysiz.'
            }, status=400)

        # Agar bog'langan bino yo'q bo'lsa, yotoqxona manzilini o'chirish
        address.delete()
        return JsonResponse({'message': 'Yotoqxona manzili muvaffaqiyatli o‘chirildi!'}, status=204)


# Binolar qo'shish uchun API view
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class AddBuildingView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def perform_create(self, serializer):
        # Bino tegishli bo'lgan yotoqxonani olish
        dormitory = get_object_or_404(DormitoryAddress, id=self.request.data.get('dormitory'))

        # Foydalanuvchini olish
        user = CustomUser.objects.filter(id=self.request.data.get('user_id')).first()

        # Binoning nomini tekshirish
        building_name = self.request.data.get('name')

        # Agar shu yotoqxonaga tegishli va shu nomga ega bino mavjud bo'lsa, xatolik yuzaga keltiradi
        if Building.objects.filter(dormitory=dormitory, name=building_name).exists():
            raise serializers.ValidationError({
                "message": f"'{building_name}' nomli bino allaqachon mavjud. Iltimos, boshqa nom tanlang."
            })

        # Agar mavjud bo'lmasa, yangi bino yaratish
        serializer.save(dormitory=dormitory, created_by=user, updated_by=user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
                return Response({
                    "status": "success",
                    "message": "Bino muvaffaqiyatli qo'shildi!"
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response({
                    "status": "error",
                    "message": str(e.detail["message"][0])
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "error",
            "message": "Xatolik yuz berdi.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Binoni "o'chirish" uchun API view (is_active ni false qilib qo'yish)
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class DeleteBuildingView(generics.UpdateAPIView):
    queryset = Building.objects.all()

    def post(self, request, *args, **kwargs):
        # Binoning ID'sini olish
        building_id = request.data.get('building_id')
        print(f"Received Building ID for deletion: {building_id}")

        # `building_id` orqali binoni olish
        building = get_object_or_404(Building, id=building_id)

        # Agar binoga biriktirilgan qavatlar mavjud bo'lsa va ularning hech bo'lmasa bittasi `is_active=True` bo'lsa, ishlamasin
        if building.floors.filter(is_active=True).exists():
            return Response({
                "status": "error",
                "message": "Bu bino faol qavatlarga ega bo'lganligi uchun o'chirib bo'lmaydi.",
            }, status=status.HTTP_400_BAD_REQUEST)

        # Barcha qavatlar `is_active=False` bo'lsa, binoni ham `is_active=False` qilib yangilash
        building.is_active = False
        building.updated_by = request.user
        building.save()

        return Response({
            "status": "success",
            "message": "Bino muvaffaqiyatli o'chirildi (faol emas deb belgilandi).",
        }, status=status.HTTP_200_OK)


# Bino etajidagi ma'lumotlarni olish uchun
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class BuildingFloorDataView(View):
    def get(self, request, *args, **kwargs):
        dormitories = DormitoryAddress.objects.prefetch_related(
            'buildings__floors__rooms').all()
        data = [{
            "dormitory_address": dormitory.address,
            "buildings": [{
                "id": building.id,
                "building_name": building.name,
                "is_active": building.is_active,  # `is_active` maydoni qo'shildi
                "address": building.dormitory.address,
                "floors": [{
                    "floor_id": floor.id,
                    "floor_number": floor.number,
                    "is_active": floor.is_active,  # `is_active` maydoni qo'shildi
                    "room_count": floor.rooms.count(),
                    "students_count": sum(room.capacity for room in floor.rooms.all()),
                    "rooms": [{
                        "room_number": room.number,
                        "student_capacity": room.capacity
                    } for room in floor.rooms.all()]
                } for floor in building.floors.all()]
            } for building in dormitory.buildings.all()]
        } for dormitory in dormitories]

        return JsonResponse({"dormitories": data})

# Qavat Qo'shish
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class AddFloorView(generics.CreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        building = get_object_or_404(Building, id=data.get('building'))
        number = data.get('number') or (Floor.objects.filter(building=building).order_by('-number').first().number + 1 if Floor.objects.filter(building=building).exists() else 1)

        data.update({'building': building.id, 'number': number, 'created_by': request.user.id, 'updated_by': request.user.id})
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"status": "success", "message": "Floor successfully created!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Qavat O'chirish
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class DeleteFloorView(generics.UpdateAPIView):
    queryset = Floor.objects.all()

    def post(self, request, *args, **kwargs):
        # JSON dan `floor_id`ni olish
        floor_id = request.data.get('floor_id')

        # `floor_id`ni print orqali chiqarish
        print(f"Received Floor ID for deletion: {floor_id}")

        # Qavatni `floor_id` orqali olish
        floor = get_object_or_404(Floor, id=floor_id)

        # Qavatni `is_active` qiymatini `False` qilib yangilash
        floor.is_active = False
        floor.updated_by = request.user
        floor.save()

        return Response({
            "status": "success",
            "message": "Qavat muvaffaqiyatli o'chirildi (faol emas deb belgilandi).",
        }, status=status.HTTP_200_OK)

# Qavatlarni json qaytarish
@method_decorator(permission_classes([IsAuthenticated]), name='dispatch')
class FloorRoomsView(generics.GenericAPIView):
    serializer_class = FloorRoomsWithBuildingAndDormitorySerializer

    def get(self, request, *args, **kwargs):
        floor = get_object_or_404(Floor, id=self.kwargs.get('floor_id'))
        serializer = self.get_serializer(floor)
        return Response(serializer.data)

