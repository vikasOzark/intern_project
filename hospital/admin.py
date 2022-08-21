from django.contrib import admin
from .models import UserProfileModel, BlogModel


# Register your models here.
@admin.register(UserProfileModel)
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'photo']
    list_filter = ['user', 'address', 'photo']
    search_fields = ['user', 'address','is_doctor']
    
@admin.register(BlogModel)
class BlogModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'category', 'summary', 'blog_image', 'content', 'modified_at', 'updated_at', 'is_draft', 'is_published']
    list_filter = ['user', 'title',  'category', 'content', 'modified_at', 'updated_at', 'is_draft', 'is_published']
    search_fields = ['user', 'title','slug', 'category',  'modified_at', 'updated_at', 'is_draft', 'is_published']
    
    # prepopulated_fields = {"slug": ("tle",)}
