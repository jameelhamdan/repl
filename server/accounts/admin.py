from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserModelAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'last_login', 'created_on', 'updated_on', )
    readonly_fields = ('last_login', 'created_on', 'updated_on')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Important dates', {'fields': ('last_login', 'created_on', 'updated_on')}),
    )
    search_fields = ['email']
    list_filter = ['is_active']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ['email']
