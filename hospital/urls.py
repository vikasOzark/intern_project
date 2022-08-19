from django.urls import path
from . import views


urlpatterns = [
    path('', views.authentication, name='index'),
    path('detail/', views.detail_view, name='detail'),
    path('logout/', views.logout_view, name='logout'),
]
