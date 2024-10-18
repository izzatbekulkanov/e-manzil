from rest_framework import serializers
from apps.e_manzil.models import DormitoryAddress, Building, Floor, Room


class DormitoryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryAddress
        fields = ['id', 'address', 'description', 'is_active']
        read_only_fields = ['created_by', 'updated_by']


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'building', 'number', 'created_by', 'updated_by', 'is_active']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'capacity']

class FloorRoomsWithBuildingAndDormitorySerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)
    building = BuildingSerializer()
    dormitory = serializers.SerializerMethodField()  # Custom method field

    class Meta:
        model = Floor
        fields = ['id', 'number', 'rooms', 'building', 'dormitory']

    def get_dormitory(self, obj):
        # Floor ob'ekti orqali Building va Building orqali Dormitory oling
        return DormitoryAddressSerializer(obj.building.dormitory).data