from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from profiles_api import models
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'firstname', 'lastname', 'phone_num', 'is_active', 'is_staff', 'is_superuser']



admin.site.register(models.UserProfile, UserAdmin)
