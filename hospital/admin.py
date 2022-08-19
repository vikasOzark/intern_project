from django.contrib import admin
from .models import UserProfileModel


# Register your models here.
@admin.register(UserProfileModel)
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'photo']
    list_filter = ['user', 'address', 'photo']
    search_fields = ['user', 'address','is_doctor']
    