from django.contrib import admin
from django.urls import path ,include
import Main_Api

urlpatterns = [
    path('', include('Main_Api.urls')),
    path('admin/', admin.site.urls)
]
