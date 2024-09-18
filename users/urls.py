from django.urls import path
from rest_framework.routers import DefaultRouter


#autenticacion
from django.urls import path

from users.auth.views.logout_usuario_view import LogoutUsuarioView
from users.auth.views.my_token_obtain_pair_view import MyTokenObtainPairView
from users.auth.views.registro_usuario_view import RegistroUsuarioView
from users.views.datos_personales_usuario_view import DatosPersonalesUsuarioViewSet
from users.views.proyecto_view import ProyectoViewSet
from users.views.role_view import RoleViewSet
from users.views.usersproject_view import UsersProjectView
from users.views.usuario_proyecto_view import UsuarioProyectoViewSet
from users.views.usuario_view import UsuarioViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path
from rest_framework.routers import DefaultRouter


# from .views import (
#     RoleViewSet, UsuarioViewSet, DatosPersonalesUsuarioViewSet, ProyectoViewSet, UsuarioProyectoViewSet, DatosCorporalesViewSet
# )


router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuarios-personales', DatosPersonalesUsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'usuario-proyectos', UsuarioProyectoViewSet)


urlpatterns = [

    path('usuarios-de-proyecto/<int:proyecto_id>/', UsersProjectView.as_view(), name='usuarios-proyecto'),

        # Autenticación JWT
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),




]

urlpatterns += router.urls
