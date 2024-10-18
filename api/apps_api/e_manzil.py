import json

from django.views.generic import View, CreateView
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model, login
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied, NotFound

from accounts.models import CustomUser
from api.forms import RoomForm
from api.serializers import DormitoryAddressSerializer, BuildingSerializer, FloorSerializer, RoomSerializer, \
    FloorRoomsWithBuildingAndDormitorySerializer
from apps.e_manzil.models import DormitoryAddress, Building, Floor, Room
import logging

logger = logging.getLogger(__name__)


class DormitoryAddressList(generics.ListCreateAPIView):
    queryset = DormitoryAddress.objects.all()
    serializer_class = DormitoryAddressSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TTJ BINOLAR
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


@method_decorator(csrf_exempt, name='dispatch')
class DormitoryAddressDeleteView(View):
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden('You do not have permission to perform this action.')

        address_id = kwargs.get('id')
        try:
            address = DormitoryAddress.objects.get(id=address_id)
            address.delete()
            return JsonResponse({'message': 'Dormitory address deleted successfully!'}, status=204)
        except DormitoryAddress.DoesNotExist:
            return JsonResponse({'error': 'Dormitory address not found.'}, status=404)


# / TTJ BINOLAR


# Binolar
class AddBuildingView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def perform_create(self, serializer):
        dormitory_id = self.request.data.get('dormitory')
        user_id = self.request.data.get('user_id')  # Foydalanuvchi ID'sini olish

        # Yotoqxona manzilini tekshirish
        try:
            dormitory = DormitoryAddress.objects.get(id=dormitory_id)
        except DormitoryAddress.DoesNotExist:
            return Response({"error": "Yotoqxona manzili topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Foydalanuvchi ID'si bo'yicha foydalanuvchini olish
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            user = None  # Agar foydalanuvchi topilmasa, `None` qiymatini beramiz

        # Serializerni saqlash
        serializer.save(
            dormitory=dormitory,
            created_by=user,
            updated_by=user
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "Bino muvaffaqiyatli qo'shildi!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"message": "GET so'rovi muvaffaqiyatli bajarildi!"}, status=status.HTTP_200_OK)


# /Binolar

class BuildingFloorDataView(View):
    def get(self, request, *args, **kwargs):
        dormitories = DormitoryAddress.objects.all()
        data = []

        for dormitory in dormitories:
            buildings_data = []
            buildings = Building.objects.filter(dormitory=dormitory)

            for building in buildings:
                floors_data = []
                floors = Floor.objects.filter(building=building)

                for floor in floors:
                    rooms = Room.objects.filter(floor=floor)
                    rooms_data = []
                    for room in rooms:
                        rooms_data.append({
                            "room_number": room.number,
                            "student_capacity": room.capacity,
                        })

                    floors_data.append({
                        "floor_id": floor.id,
                        "floor_number": floor.number,
                        "room_count": rooms.count(),
                        "students_count": sum(room.capacity for room in rooms),
                        "rooms": rooms_data
                    })

                buildings_data.append({
                    "id": building.id,  # Add this line to include building ID
                    "building_name": building.name,
                    "address": building.dormitory.address,
                    "floors": floors_data
                })

            data.append({
                "dormitory_address": dormitory.address,
                "buildings": buildings_data
            })

        return JsonResponse({"dormitories": data})


class AddFloorView(generics.CreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        building_id = data.get('building')
        number = data.get('number')

        if not building_id:
            return Response({"status": "error", "message": "Building ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            return Response({"status": "error", "message": "Building not found"},
                            status=status.HTTP_404_NOT_FOUND)

        # Avvalgi qavatlardan keyingi raqamni hisoblash
        if number is None:
            last_floor = Floor.objects.filter(building=building).order_by('-number').first()
            number = last_floor.number + 1 if last_floor else 1

        # Ma'lumotlarga building_id va foydalanuvchi ID-larini qo'shish
        data['building'] = building.id
        data['number'] = number
        data['created_by'] = request.user.id
        data['updated_by'] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": "success", "message": "Floor successfully created!", "data": serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        return Response({"status": "error", "message": "Validation failed", "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class FloorRoomsView(generics.GenericAPIView):
    serializer_class = FloorRoomsWithBuildingAndDormitorySerializer

    def get(self, request, *args, **kwargs):
        floor_id = self.kwargs.get('floor_id')
        if not floor_id:
            return Response({'detail': 'Qavat ID-si talab qilinadi'}, status=400)

        try:
            floor = Floor.objects.get(id=floor_id)
        except Floor.DoesNotExist:
            return Response({'detail': 'Qavat topilmadi'}, status=404)

        # Avval `Floor` ning `Building` va `Dormitory` ob'ektlarini olish
        building = floor.building
        dormitory = building.dormitory

        # `Floor`, `Building`, va `Dormitory` ob'ektlarini serializatsiya qilish
        serializer = self.get_serializer(floor)
        return Response(serializer.data)


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm

    def form_valid(self, form):
        room = form.save()
        response_data = {
            'status': 'success',
            'message': f"Xona {room.number} muvaffaqiyatli qo'shildi.",
            'room_id': room.id
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        response_data = {
            'status': 'error',
            'message': 'Xona yaratishda xatolik yuz berdi.',
            'errors': errors
        }
        return JsonResponse(response_data)
