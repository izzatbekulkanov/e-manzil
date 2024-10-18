from rest_framework_simplejwt.tokens import RefreshToken
from accounts.edu_models import University, Specialty, GroupUniver, Department, EducationType, EducationForm, Curriculum, \
    Level, Semester, EducationYear
import random
import string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with no username field."""

    def _generate_random_username(self):
        """Generate a random 9-digit number."""
        random_number = ''.join(random.choices(string.digits, k=12))
        return '309' + random_number  # Adding '309' as prefix

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a CustomUser with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Gender(models.Model):
    code = models.CharField(max_length=20, verbose_name="Jins kodi")
    name = models.CharField(max_length=255, verbose_name="Jins nomi")

    def __str__(self):
        return self.name


class StaffPosition(models.Model):
    code = models.CharField(max_length=20, verbose_name="Xodim o'rni kodi")
    name = models.CharField(max_length=255, verbose_name="Xodim o'rni nomi")

    def __str__(self):
        return self.name


class EmployeeStatus(models.Model):
    code = models.CharField(max_length=20, verbose_name="Xodim holati kodi")
    name = models.CharField(max_length=255, verbose_name="Xodim holati nomi")

    def __str__(self):
        return self.name


class EmployeeType(models.Model):
    code = models.CharField(max_length=20, verbose_name="Xodim turi kodi")
    name = models.CharField(max_length=255, verbose_name="Xodim turi nomi")

    def __str__(self):
        return self.name


class AcademicRank(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ilmiy unvon kodi")
    name = models.CharField(max_length=255, verbose_name="Ilmiy unvon nomi")

    def __str__(self):
        return self.name


class AcademicDegree(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ilmiy daraja kodi")
    name = models.CharField(max_length=255, verbose_name="Ilmiy daraja nomi")

    def __str__(self):
        return self.name


class EmploymentForm(models.Model):
    code = models.CharField(max_length=20, verbose_name="Bandlik shakli kodi")
    name = models.CharField(max_length=255, verbose_name="Bandlik shakli nomi")

    def __str__(self):
        return self.name


class EmploymentStaff(models.Model):
    code = models.CharField(max_length=20, verbose_name="Bandlik hodimlar kodi")
    name = models.CharField(max_length=255, verbose_name="Bandlik hodimlar nomi")

    def __str__(self):
        return self.name


class PaymentForm(models.Model):
    code = models.CharField(max_length=20, verbose_name="To'lov turi")
    name = models.CharField(max_length=255, verbose_name="To'lov nomi")

    def __str__(self):
        return self.name


class SocialCategory(models.Model):
    code = models.CharField(max_length=20, verbose_name="Talaba holati code")
    name = models.CharField(max_length=255, verbose_name="Talaba holati nomi")

    def __str__(self):
        return self.name


class Country(models.Model):
    code = models.CharField(max_length=20, verbose_name="Mamlakat kodi")
    name = models.CharField(max_length=255, verbose_name="Mamlakat nomi")

    def __str__(self):
        return self.name


class Province(models.Model):
    code = models.CharField(max_length=20, verbose_name="Viloyat kodi")
    name = models.CharField(max_length=255, verbose_name="Viloyat nomi")

    def __str__(self):
        return self.name


class District(models.Model):
    code = models.CharField(max_length=20, verbose_name="Tuman kodi")
    name = models.CharField(max_length=255, verbose_name="Tuman nomi")

    def __str__(self):
        return self.name


class Citizenship(models.Model):
    code = models.CharField(max_length=20, verbose_name="Fuqarolik kodi")
    name = models.CharField(max_length=255, verbose_name="Fuqarolik nomi")

    def __str__(self):
        return self.name


class StudentType(models.Model):
    code = models.CharField(max_length=20, verbose_name="Talaba turi kodi")
    name = models.CharField(max_length=255, verbose_name="Talaba turi nomi")

    def __str__(self):
        return self.name


class StudentStatus(models.Model):
    code = models.CharField(max_length=20, verbose_name="Talabaning holati kodi")
    name = models.CharField(max_length=255, verbose_name="Talabaning holati nomi")

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    code = models.CharField(max_length=20, verbose_name="Talabaning turar joyi kodi")
    name = models.CharField(max_length=255, verbose_name="Talabaning turar joyi nomi")

    def __str__(self):
        return self.name


class Roles(models.Model):
    code = models.CharField(max_length=20, verbose_name="role kodi")
    name = models.CharField(max_length=255, verbose_name="role nomi")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    type_choice = (
        ("1", "Talaba"),
        ("2", "Hodim"),
        ("3", "O'qituvchi"),
    )
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, verbose_name="Universitet")
    full_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="To'liq ism")
    short_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Qisqa ism")
    first_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Ism")
    second_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Familia")
    third_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="Otasining ismi")
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, verbose_name="Jins", blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan kun")
    image = models.URLField(blank=True, null=True, max_length=255, verbose_name="Rasm")
    imageFile = models.ImageField(upload_to='students/%Y/%m/%d', default='default/user.png',
                                  verbose_name="Rasmi faylda", blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name="Davlat", null=True, blank=True)
    address = models.TextField(null=True, blank=True, verbose_name="Manzili")
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, verbose_name="Viloyat", null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, verbose_name="Tuman", null=True, blank=True)
    citizenship = models.ForeignKey(Citizenship, on_delete=models.SET_NULL, verbose_name="Fuqarolik", null=True,
                                    blank=True)
    studentStatus = models.ForeignKey(StudentStatus, on_delete=models.SET_NULL, verbose_name="Talaba holati", null=True,
                                      blank=True)
    educationForm = models.ForeignKey(EducationForm, on_delete=models.SET_NULL, verbose_name="Ta'lim shakli", null=True,
                                      blank=True)
    educationType = models.ForeignKey(EducationType, on_delete=models.SET_NULL, verbose_name="Ta'lim turi", null=True,
                                      blank=True)
    employmentStaff = models.ForeignKey(EmploymentStaff, on_delete=models.SET_NULL, verbose_name="Bandlik hodimlar",
                                        null=True, blank=True)
    employmentForm = models.ForeignKey(EmploymentForm, on_delete=models.SET_NULL, verbose_name="Bandlik shakli",
                                       null=True, blank=True)
    paymentForm = models.ForeignKey(PaymentForm, on_delete=models.SET_NULL, verbose_name="To'lov turi", null=True,
                                    blank=True)
    studentType = models.ForeignKey(StudentType, on_delete=models.SET_NULL, verbose_name="Talaba turi", null=True,
                                    blank=True)
    socialCategory = models.ForeignKey(SocialCategory, on_delete=models.SET_NULL, verbose_name="Talaba Holati",
                                       null=True, blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, verbose_name="Turar joyi", blank=True,
                                      null=True, )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name="Fakultet", blank=True,
                                   null=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.SET_NULL, verbose_name="O'quv rejasi", null=True,
                                   blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, verbose_name="Mutaxassislik", null=True,
                                  blank=True)
    group = models.ForeignKey(GroupUniver, on_delete=models.SET_NULL, verbose_name="Guruh", null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, verbose_name="Bosqich", null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, verbose_name="Semestr", null=True, blank=True)
    educationYear = models.ForeignKey(EducationYear, on_delete=models.SET_NULL, verbose_name="O'quv yili", null=True,
                                      blank=True)
    year_of_enter = models.CharField(null=True, blank=True, max_length=255, verbose_name="Kirish yili")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    hash = models.CharField(null=True, blank=True, max_length=255, verbose_name="Hash")
    now_role = models.CharField(null=True, blank=True, max_length=255,
                                verbose_name="Foydalanuvchining hozirgi vaqtdagi roli")
    username = models.CharField(null=True, blank=True, max_length=255, unique=True)
    email = models.EmailField(('email address'), unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(null=True, max_length=15, blank=True)
    password_save = models.CharField(('password save'), max_length=128, blank=True,
                                     null=True)  # Added password_save field
    employeeStatus = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, verbose_name="Xodimholati",
                                       blank=True, null=True)
    academikRank = models.ForeignKey(AcademicRank, on_delete=models.SET_NULL, verbose_name="Ilmiy Unvon", blank=True,
                                     null=True)
    academicDegree = models.ForeignKey(AcademicDegree, on_delete=models.SET_NULL, verbose_name="Ilmiy Daraja",
                                       blank=True, null=True)
    contractDate = models.CharField(null=True, blank=True, max_length=255, verbose_name="Shartnoma sanasi")
    staffPosition = models.ForeignKey(StaffPosition, on_delete=models.SET_NULL, verbose_name="Xodimo'rni", blank=True,
                                      null=True, related_name='staffposition')
    user_type = models.CharField(_('Type'), choices=type_choice, default="1", max_length=20, blank=True, null=True)
    hemis_role = models.ManyToManyField(Roles, verbose_name="Rollar", blank=True)
    employeeType = models.ForeignKey(EmployeeType, on_delete=models.SET_NULL, verbose_name="Xodim turi", blank=True,
                                     null=True)
    is_student = models.BooleanField(default=False, verbose_name="Talaba", blank=True, null=True)
    is_employee = models.BooleanField(default=False, verbose_name="Hodim", blank=True, null=True)
    is_followers_book = models.BooleanField(default=False, verbose_name="is_followers_book")
    last_login = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    token = models.TextField(null=True, blank=True)
    # Additional fields for the university
    passport_serial = models.CharField(max_length=20, null=True, blank=True)
    passport_issue_date = models.DateField(null=True, blank=True)
    passport_jshshir = models.CharField(max_length=20, null=True, blank=True)
    # Additional field
    hemis_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="To'liq ID")
    # Ijtimoiy tarmoqlar

    telegram = models.URLField(null=True, blank=True, verbose_name="Telegram profil havolasi")
    instagram = models.URLField(null=True, blank=True, verbose_name="Instagram profil havolasi")
    facebook = models.URLField(null=True, blank=True, verbose_name="Facebook profil havolasi")

    def __str__(self):
        return self.username  # yoki return self.email yoki return self.full_name

    def get_session_auth_hash(self):
        return "some_hash"  # Sizning xohlagan hash algoritmingizni ishlatishingiz mumkin

    USERNAME_FIELD = 'email'  # Users login in with their email
    REQUIRED_FIELDS = ['username']  # username required field

    def get_jwt_token(self):
        # Foydalanuvchi uchun JWT token yaratish
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
