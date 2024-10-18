# api/forms.py
from django import forms
from apps.e_manzil.models import DormitoryAddress, Room

class DormitoryAddressForm(forms.ModelForm):
    class Meta:
        model = DormitoryAddress
        fields = ['address', 'description', 'created_by', 'is_active']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['floor', 'number', 'capacity']
        # 'note' maydoni olib tashlandi