from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import reports
from users.views.usuario_view import RegistroUsuarioView
from users.auth.views.logout_usuarios_view import LogoutUsuarioView
from rest_framework_simplejwt.views import TokenRefreshView
from users.auth.views.login_usuarios_view import LoginUsuarioView, MyTokenObtainPairView

# Importa los enrutadores de las aplicaciones
from users.urls import router as users_router
from habits.urls import router as habits_router
# from health.urls import router as health_router

# Crea un enrutador principal
api_router = DefaultRouter()

# Combina los enrutadores de users, habits y health en el enrutador principal
api_router.registry.extend(users_router.registry)
api_router.registry.extend(habits_router.registry)
# api_router.registry.extend(health_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('reports/', include('reports.urls')),
    path('health/', include('health.urls')),
    path('users/', include('users.urls')),
    path('habits/', include('habits.urls')),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginUsuarioView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
