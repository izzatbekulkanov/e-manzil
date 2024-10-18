from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import CustomUser

User = get_user_model()

class DormitoryAddress(models.Model):
    address = models.CharField(max_length=255, unique=True, verbose_name="Yotoqxona manzili")
    description = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='dormitory_address_created', verbose_name="Yaratuvchi")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='dormitory_address_updated', verbose_name="Yangilovchi")
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")

    class Meta:
        verbose_name = "Yotoqxona manzili"
        verbose_name_plural = "Yotoqxona manzillari"

    def __str__(self):
        return self.address

class Building(models.Model):
    dormitory = models.ForeignKey(DormitoryAddress, on_delete=models.CASCADE, related_name='buildings', verbose_name="Manzilga bog'langan bino")
    name = models.CharField(max_length=100, verbose_name="Binoning nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Binoning qo'shimcha tavsifi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='building_created', verbose_name="Yaratuvchi")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='building_updated', verbose_name="Yangilovchi")
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")

    class Meta:
        verbose_name = "Bino"
        verbose_name_plural = "Binolar"

    def __str__(self):
        return f"{self.name} - {self.dormitory.address}"

class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors', verbose_name="Binoga bog'langan qavat")
    number = models.PositiveIntegerField(verbose_name="Qavat raqami")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='floor_created', verbose_name="Yaratuvchi")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='floor_updated', verbose_name="Yangilovchi")
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")

    class Meta:
        verbose_name = "Qavat"
        verbose_name_plural = "Qavatlar"
        ordering = ['number']

    def __str__(self):
        return f"Qavat {self.number} - {self.building.name}"

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms', verbose_name="Qavatga bog'langan xona")
    number = models.CharField(max_length=10, verbose_name="Xona raqami")
    capacity = models.PositiveIntegerField(verbose_name="Xonadagi talabalar sig‘imi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='room_created', verbose_name="Yaratuvchi")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='room_updated', verbose_name="Yangilovchi")
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ['number']

    def __str__(self):
        return f"Xona {self.number} - Qavat {self.floor.number}"
