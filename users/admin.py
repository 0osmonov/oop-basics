from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'birthdate',
        'registration_source',
        'is_staff',
        'is_active',
        'last_login',
    )
    list_filter = ('is_staff', 'is_active', 'registration_source')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('birthdate', 'registration_source')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('birthdate', 'registration_source')}),
    )
