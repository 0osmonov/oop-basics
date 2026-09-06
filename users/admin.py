from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'birthdate', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('birthdate',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('birthdate',)}),
    )
