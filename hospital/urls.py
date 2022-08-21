from django.urls import path
from . import views


urlpatterns = [
    path('', views.authentication, name='index'),
    path('detail/', views.detail_view, name='detail'),
    path('logout/', views.logout_view, name='logout'),
    path('blog_view/<slug:slug>', views.blog_view, name='blog_view'),
    path('blog_create/', views.blog_create, name='blog_create'),
    path('save_draft/', views.save_draft, name='save_draft'),
    path('all_blogs/', views.all_blogs, name='all_blogs'),
]
