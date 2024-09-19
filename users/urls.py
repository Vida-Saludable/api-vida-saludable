from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.role_view import RoleViewSet
from .views.usuario_view import UsuarioViewSet
from .views.datos_personales_usuario_view import DatosPersonalesUsuarioViewSet
from .views.proyecto_view import ProyectoViewSet
from .views.usuario_proyecto_view import UsuarioProyectoViewSet
from health.views.datos_corporales_view import DatosCorporalesViewSet
from .views.usersproject_view import UsersProjectView


# Crea un enrutador para la aplicación users
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuarios-personales', DatosPersonalesUsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'usuario-proyectos', UsuarioProyectoViewSet)
router.register(r'datos-corporales', DatosCorporalesViewSet)

urlpatterns = [
    path('usuarios-de-proyecto/<int:proyecto_id>/', UsersProjectView.as_view(), name='usuarios-proyecto'),
]

urlpatterns += router.urls
