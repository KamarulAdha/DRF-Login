from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from profiles_api import models

from django.utils.translation import gettext as _

# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'firstname', 'lastname', 'phone_num', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('firstname', 'lastname', 'phone_num')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstname', 'lastname', 'phone_num')
        }),
    )





admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.ExtraInfo)
