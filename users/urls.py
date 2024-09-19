from django.urls import path
from rest_framework.routers import DefaultRouter




#autenticacion
from django.urls import path

from users.views.usersproject_view import UsersProjectView
from views.usuario_view import RegistroUsuarioView
from auth.views.logout_usuarios_view import LogoutUsuarioView
from rest_framework_simplejwt.views import TokenRefreshView
from auth.views.login_usuarios_view import MyTokenObtainPairView

from django.urls import path
from rest_framework.routers import DefaultRouter

# from api.habits.viewhabitspatient import  RegistroHabitosView, ReporteAguaView, ReporteAireView, ReporteEjercicioPorcentajeView, ReporteEjercicioTipoView, ReporteEjercicioView, ReporteEsperanzaPorcentajeView, ReporteHorasDormidasView, ReportePorcentajeDescansoView, ReporteSolView
# from .views import (
#     RoleViewSet, UsuarioViewSet, DatosPersonalesUsuarioViewSet, AlimentacionViewSet, AguaViewSet, EsperanzaViewSet, 
#     SolViewSet, AireViewSet, DormirViewSet, DespertarViewSet, EjercicioViewSet, ProyectoViewSet, UsuarioProyectoViewSet, DatosCorporalesViewSet, DatosHabitosViewSet
# )

from views.role_view import RoleViewSet
from views.usuario_view import UsuarioViewSet
from views.datos_personales_usuario_view import DatosPersonalesUsuarioViewSet
from views.proyecto_view import ProyectoViewSet
from views.usuario_proyecto_view import UsuarioProyectoViewSet
from health.views.datos_corporales_view import DatosCorporalesViewSet



router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuarios-personales', DatosPersonalesUsuarioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'usuario-proyectos', UsuarioProyectoViewSet)
router.register(r'datos-corporales', DatosCorporalesViewSet)


urlpatterns = [

    path('usuarios-de-proyecto/<int:proyecto_id>/', UsersProjectView.as_view(), name='usuarios-proyecto'),

        # Autenticación JWT
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),




]

urlpatterns += router.urls
