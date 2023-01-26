from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework import routers

# Change the actual paths here to their respective locations :
router = routers.DefaultRouter()
router.register('Main_Api', views.Main_ModelViews)
urlpatterns = [
    path('', views.home),
    path('api/', include(router.urls)),
    path('form/', views.Uform, name='UserForm'),
]
