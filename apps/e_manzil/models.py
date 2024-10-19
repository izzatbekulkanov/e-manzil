from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


# OopCompanion:suppressRename

User = get_user_model()


# Yotoqxona manzillarini saqlash uchun model
class DormitoryAddress(models.Model):
    address = models.CharField(max_length=255, unique=True, verbose_name="Yotoqxona manzili")  # Yotoqxonaning manzili
    description = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha tavsif")  # Qo'shimcha tavsif
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")  # Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Yangilangan vaqt
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='dormitory_address_created', verbose_name="Yaratuvchi")  # Yaratuvchi foydalanuvchi
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='dormitory_address_updated', verbose_name="Yangilovchi")  # Yangilovchi foydalanuvchi
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")  # Faol yoki nofaol holati

    class Meta:
        verbose_name = "Yotoqxona manzili"
        verbose_name_plural = "Yotoqxona manzillari"

    def __str__(self):
        return self.address  # Ob'ektni chiqarishda manzilni qaytaradi


# Yotoqxonaga tegishli binolarni saqlash uchun model
class Building(models.Model):
    dormitory = models.ForeignKey(DormitoryAddress, on_delete=models.CASCADE, related_name='buildings', verbose_name="Manzilga bog'langan bino")  # Bino tegishli bo'lgan yotoqxona manzili
    name = models.CharField(max_length=100, verbose_name="Binoning nomi")  # Binoning nomi
    description = models.TextField(blank=True, null=True, verbose_name="Binoning qo'shimcha tavsifi")  # Qo'shimcha tavsif
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")  # Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Yangilangan vaqt
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='building_created', verbose_name="Yaratuvchi")  # Yaratuvchi foydalanuvchi
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='building_updated', verbose_name="Yangilovchi")  # Yangilovchi foydalanuvchi
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")  # Faol yoki nofaol holati

    class Meta:
        verbose_name = "Bino"
        verbose_name_plural = "Binolar"

    def __str__(self):
        return f"{self.name} - {self.dormitory.address}"  # Ob'ektni chiqarishda bino nomi va yotoqxona manzilini qaytaradi


# Binoga tegishli qavatlarni saqlash uchun model
class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors', verbose_name="Binoga bog'langan qavat")  # Qavat tegishli bo'lgan bino
    number = models.PositiveIntegerField(verbose_name="Qavat raqami")  # Qavatning raqami (masalan, 1, 2, 3...)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")  # Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Yangilangan vaqt
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='floor_created', verbose_name="Yaratuvchi")  # Yaratuvchi foydalanuvchi
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='floor_updated', verbose_name="Yangilovchi")  # Yangilovchi foydalanuvchi
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")  # Faol yoki nofaol holati

    class Meta:
        verbose_name = "Qavat"
        verbose_name_plural = "Qavatlar"
        ordering = ['number']  # Qavatlar tartibda ko'rsatiladi (raqam bo'yicha)

    def __str__(self):
        return f"Qavat {self.number} - {self.building.name}"  # Ob'ektni chiqarishda qavat va bino nomini qaytaradi


# Qavatlarga tegishli xonalarni saqlash uchun model
class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms', verbose_name="Qavatga bog'langan xona")  # Xona tegishli bo'lgan qavat
    number = models.CharField(max_length=10, verbose_name="Xona raqami")  # Xona raqami (masalan, 101, 102...)
    capacity = models.PositiveIntegerField(verbose_name="Xonadagi talabalar sig‘imi")  # Xonaning sig'imi (nechta talaba sig'ishi mumkin)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratuvchi vaqt")  # Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")  # Yangilangan vaqt
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='room_created', verbose_name="Yaratuvchi")  # Yaratuvchi foydalanuvchi
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='room_updated', verbose_name="Yangilovchi")  # Yangilovchi foydalanuvchi
    is_active = models.BooleanField(default=True, verbose_name="Faol yoki nofaol")  # Faol yoki nofaol holati

    # Talabalar yoki hodimlarni bog'lash uchun maydon
    occupants = models.ManyToManyField(CustomUser, blank=True, related_name='assigned_rooms', verbose_name="Xonadagi talaba yoki hodimlar") #`CustomUser` modelidan foydalanuvchilarni (talabalar yoki hodimlar) bog'lash uchun

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ['number']  # Xonalar raqam bo'yicha tartiblanadi

    def __str__(self):
        return f"Xona {self.number} - Qavat {self.floor.number}"  # Ob'ektni chiqarishda xona va qavatni qaytaradi


