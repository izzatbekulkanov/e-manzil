from django.db import models
from django.utils import timezone

class University(models.Model):
    code = models.CharField(max_length=20, verbose_name="Universitet kodi")
    name = models.CharField(max_length=255, verbose_name="Universitet nomi")
    api_url = models.URLField(verbose_name="API URL", null=True, blank=True)
    api_token = models.CharField(max_length=255, verbose_name="API Token", null=True, blank=True)
    student_url = models.URLField(verbose_name="Student URL", null=True, blank=True)
    employee_url = models.URLField(verbose_name="Xodimlar URL", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return self.name


class Department(models.Model):
    STRUCTURE_TYPE_CHOICES = [
        ('10', 'Boshqa'),
        ('11', 'Fakultet'),
        ('12', 'Kafedra'),
        ('13', 'Bo‘lim'),
        ('14', 'Boshqarma'),
        ('15', 'Markaz'),
        ('16', 'Rektorat'),
    ]

    codeID = models.CharField(max_length=255, verbose_name="Fakultet ID")
    name = models.CharField(max_length=255, verbose_name="Fakultet nomi")
    code = models.CharField(max_length=20, verbose_name="Fakultet kodi")
    parent = models.CharField(max_length=20, null=True, blank=True, verbose_name="Boshqa fakultet")
    active = models.BooleanField(default=True, verbose_name="Faol")
    structure_type = models.CharField(
        max_length=2,
        choices=STRUCTURE_TYPE_CHOICES,
        verbose_name='Bo‘lim turi'
    )

    def __str__(self):
        return f"{self.name} - {self.get_structure_type_display()}"


class Specialty(models.Model):
    codeID = models.CharField(max_length=255, verbose_name="Yo'nalish ID raqami")
    name = models.CharField(max_length=255, verbose_name="Yo'nalish nomi")
    code = models.CharField(max_length=50, verbose_name="Yo'nalish kodi")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Fakultet")
    educationType = models.ForeignKey('EducationType', on_delete=models.CASCADE, verbose_name="Ta'lim turi")

    def __str__(self):
        return self.name


class Semester(models.Model):
    code = models.CharField(max_length=20, verbose_name="Semestr kodi")
    name = models.CharField(max_length=255, verbose_name="Semestr nomi")

    def __str__(self):
        return self.name


class Level(models.Model):
    code = models.CharField(max_length=20, verbose_name="Bosqich kodi")
    name = models.CharField(max_length=255, verbose_name="Bosqich nomi")

    def __str__(self):
        return self.name


class EducationLang(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ta'lim tili kodi")
    name = models.CharField(max_length=255, verbose_name="Ta'lim tili nomi")

    def __str__(self):
        return self.name


class EducationForm(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ta'lim shakli kodi")
    name = models.CharField(max_length=255, verbose_name="Ta'lim shakli nomi")

    def __str__(self):
        return self.name


class EducationType(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ta'lim turi kodi")
    name = models.CharField(max_length=255, verbose_name="Ta'lim turi nomi")

    def __str__(self):
        return self.name


class EducationYear(models.Model):
    code = models.CharField(max_length=20, verbose_name="O'quv yili kodi")
    name = models.CharField(max_length=255, verbose_name="O'quv yili nomi")

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    codeID = models.CharField(max_length=20, verbose_name="O'quv reja ID", null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name="Yo'nalish")
    educationType = models.ForeignKey(EducationType, on_delete=models.CASCADE, verbose_name="Ta'lim turi")
    educationForm = models.ForeignKey(EducationForm, on_delete=models.CASCADE, verbose_name="Ta'lim shakli")
    name = models.CharField(max_length=255, verbose_name="Dastur nomi")
    semester_count = models.IntegerField(verbose_name="Semestrlar soni", null=True, blank=True)
    education_period = models.IntegerField(verbose_name="Ta'lim davomi (Yilda)", null=True, blank=True)

    def __str__(self):
        return self.name


class GroupUniver(models.Model):
    codeID = models.CharField(max_length=255, verbose_name="Guruh nomi")
    name = models.CharField(max_length=255, verbose_name="Guruh nomi")
    educationLang = models.ForeignKey(EducationLang, on_delete=models.CASCADE, verbose_name="Ta'lim tili")
    code = models.CharField(max_length=20, verbose_name="Guruh kodi", blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Fakultet")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name="Mutaxassislik")
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, verbose_name="O'quv rejasi", blank=True, null=True)

    def __str__(self):
        return self.name


class SubjectDetail(models.Model):
    trainingType = models.ForeignKey('TrainingType', on_delete=models.CASCADE, verbose_name="Ta'lim turi")
    academic_load = models.IntegerField(verbose_name="Akademik yuk")

    def __str__(self):
        return f"{self.trainingType.name} - {self.academic_load}"


class TrainingType(models.Model):
    code = models.CharField(max_length=20, verbose_name="Ta'lim turi kodi")
    name = models.CharField(max_length=255, verbose_name="Ta'lim turi nomi")

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Fan", related_name="subject_fan")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="Semestr")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Bo'lim")
    subjectDetails = models.ManyToManyField(SubjectDetail, verbose_name="Fan tafsilotlari")
    total_acload = models.IntegerField(verbose_name="Umumiy akademik yuk")
    credit = models.IntegerField(verbose_name="Kredit", null=True, blank=True)
    resource_count = models.IntegerField(verbose_name="Resurslar soni", null=True, blank=True)
    in_group = models.IntegerField(verbose_name="Guruhda", null=True, blank=True)
    at_semester = models.BooleanField(default=True, verbose_name="Semestrda", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.subject} - {self.semester.name}"
