from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import (
    Gender, StaffPosition, EmployeeStatus, EmployeeType, AcademicRank, AcademicDegree,
    EmploymentForm, EmploymentStaff, PaymentForm, SocialCategory, Country, Province, District,
    Citizenship, StudentType, StudentStatus, Accommodation, Roles, CustomUser
)
from accounts.edu_models import (
    University, Department, Specialty, Semester, Level, EducationLang, EducationForm,
    EducationType, EducationYear, Curriculum, GroupUniver, SubjectDetail, TrainingType, Subject
)


# Dynamic fieldsets generator
def get_fieldsets():
    personal_info_fields = (
        'full_name', 'short_name', 'first_name', 'second_name', 'third_name', 'gender',
        'birth_date', 'image', 'country', 'address', 'province', 'district', 'citizenship',
        'studentStatus', 'educationForm', 'educationType', 'employmentStaff', 'employmentForm',
        'paymentForm', 'studentType', 'socialCategory', 'accommodation', 'department',
        'curriculum', 'specialty', 'group', 'level', 'semester', 'educationYear', 'year_of_enter'
    )

    return (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': personal_info_fields}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login',)}))


# Custom User Admin Configuration
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = get_fieldsets()
    readonly_fields = ('created_at', 'updated_at',)  # Add readonly fields here

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if change:
            self.message_user(request, "User details updated")
        else:
            self.message_user(request, "New user created")
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)


# General ModelAdmin configuration with search and list display
class BaseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


# Register other models
admin.site.register(Gender, BaseAdmin)
admin.site.register(StaffPosition, BaseAdmin)
admin.site.register(EmployeeStatus, BaseAdmin)
admin.site.register(EmployeeType, BaseAdmin)
admin.site.register(AcademicRank, BaseAdmin)
admin.site.register(AcademicDegree, BaseAdmin)
admin.site.register(EmploymentForm, BaseAdmin)
admin.site.register(EmploymentStaff, BaseAdmin)
admin.site.register(PaymentForm, BaseAdmin)
admin.site.register(SocialCategory, BaseAdmin)
admin.site.register(Country, BaseAdmin)
admin.site.register(Province, BaseAdmin)
admin.site.register(District, BaseAdmin)
admin.site.register(Citizenship, BaseAdmin)
admin.site.register(StudentType, BaseAdmin)
admin.site.register(StudentStatus, BaseAdmin)
admin.site.register(Accommodation, BaseAdmin)
admin.site.register(Roles, BaseAdmin)


# Inline Models
class CurriculumInline(admin.TabularInline):
    model = Curriculum
    extra = 1
    fields = ('name', 'specialty', 'educationType', 'educationForm', 'semester_count', 'education_period')


# Custom ModelAdmin with multiple features
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'api_url', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name', 'code', 'api_url', 'api_token', 'student_url', 'employee_url', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'structure_type', 'active')
    search_fields = ('name', 'code', 'parent')
    list_filter = ('active', 'structure_type')
    readonly_fields = ('codeID',)
    fieldsets = (
        (None, {'fields': ('name', 'code', 'structure_type', 'active', 'parent')}),
        ('Identification', {'fields': ('codeID',)}),
    )


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'educationType')
    search_fields = ('name', 'code')
    list_filter = ('department', 'educationType')
    inlines = [CurriculumInline]


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'educationType', 'educationForm', 'semester_count', 'education_period')
    search_fields = ('name', 'specialty__name', 'educationType__name', 'educationForm__name')
    list_filter = ('specialty', 'educationType', 'educationForm')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'semester', 'department', 'total_acload', 'credit', 'resource_count', 'in_group')
    search_fields = ('subject__name', 'semester__name', 'department__name')
    list_filter = ('semester', 'department')
    filter_horizontal = ('subjectDetails',)


# Custom admin actions
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = "Mark selected as active"


@admin.register(SubjectDetail)
class SubjectDetailAdmin(admin.ModelAdmin):
    list_display = ('trainingType', 'academic_load')
    search_fields = ('trainingType__name',)
    list_filter = ('trainingType',)
    actions = [make_active]


@admin.register(TrainingType)
class TrainingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(EducationLang)
class EducationLangAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(EducationForm)
class EducationFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(EducationType)
class EducationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(EducationYear)
class EducationYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
