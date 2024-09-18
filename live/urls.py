

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('api/', include('health.urls')),


]
