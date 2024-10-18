from django.contrib import admin
from .models import DormitoryAddress, Building, Floor, Room


class BuildingInline(admin.TabularInline):
    model = Building
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    readonly_fields = ('created_at', 'updated_at')



class DormitoryAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active')
    search_fields = ('address', 'description')
    list_filter = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('address', 'description', 'is_active')
        }),
        ('Tahrir qilish', {
            'classes': ('collapse',),
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
        }),
    )
    inlines = [BuildingInline]

class BuildingInline(admin.TabularInline):
    model = Building
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'dormitory', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at', 'updated_at', 'dormitory')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'dormitory', 'description', 'is_active')
        }),
        ('Tahrir qilish', {
            'classes': ('collapse',),
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
        }),
    )
    inlines = [FloorInline]

class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class FloorAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active')
    search_fields = ('number',)
    list_filter = ('is_active', 'created_at', 'updated_at', 'building')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('number', 'building', 'is_active')
        }),
        ('Tahrir qilish', {
            'classes': ('collapse',),
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
        }),
    )
    inlines = [RoomInline]

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1
    readonly_fields = ('created_at', 'updated_at')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'capacity', 'created_at', 'updated_at', 'created_by', 'updated_by', 'is_active')
    search_fields = ('number',)
    list_filter = ('is_active', 'created_at', 'updated_at', 'floor')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('number', 'floor', 'capacity', 'is_active')
        }),
        ('Tahrir qilish', {
            'classes': ('collapse',),
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
        }),
    )

admin.site.register(DormitoryAddress, DormitoryAddressAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)

