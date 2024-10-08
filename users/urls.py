from django.urls import path # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore

from .views.role_view import RoleViewSet
from .views.usuario_view import EditarPacienteView, ListaUsuariosView, UsuarioViewSet, ListaPacientesView
from .views.datos_personales_usuario_view import DatosPersonalesUsuarioViewSet, ListaDatosPersonalesUsuarioView
from .views.proyecto_view import ProyectoViewSet
from .views.usuario_proyecto_view import ListaProyectosPorUsuarioView, UsuarioProyectoViewSet
# from health.views.datos_corporales_view import DatosCorporalesViewSet
from .views.usersproject_view import UsersProjectView


# Crea un enrutador para la aplicación users
router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuarios-personales', DatosPersonalesUsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'usuario-proyectos', UsuarioProyectoViewSet)
# router.register(r'datos-corporales', DatosCorporalesViewSet)

urlpatterns = [
    path('usuarios-de-proyecto/<int:proyecto_id>/', UsersProjectView.as_view(), name='usuarios-proyecto'),

    #LISTA LOS PROYECTO DE CADA USUARIO
    path('proyectos-de-usuarios/<int:usuario_id>/', ListaProyectosPorUsuarioView.as_view(), name='lista-proyectos-usuario'),

    # LISTA USUARIOS EXCLUYENDO AL ROL PACEINTE
    path('lista-usuarios/', ListaUsuariosView.as_view(), name='lista-usuarios'),

    # LISTA PACIENTES
    path('lista-pacientes/', ListaPacientesView.as_view(), name='lista-pacientes'),

    # LISTA DATOS PERSONALES DE POR USUARIO
    path('lista-datos-personales/<int:usuario_id>/', ListaDatosPersonalesUsuarioView.as_view(), name='lista_datos_personales_usuario'),

    # EDITAR PACIENTES
    path('editar-paciente/<int:pk>/', EditarPacienteView.as_view(), name='editar-paciente'),
    
]

urlpatterns += router.urls
