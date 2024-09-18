from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UsuarioViewSet, DatosPersonalesUsuarioViewSet, AlimentacionViewSet, AguaViewSet, EsperanzaViewSet, 
    SolViewSet, AireViewSet, DormirViewSet, DespertarViewSet, EjercicioViewSet, ProyectoViewSet, UsuarioProyectoViewSet, DatosCorporalesViewSet, DatosHabitosViewSet
)
from .health.viewindicatorhealthy import IndicadoresSaludPorUsuarioView
from .health.viewindicatormainwithfinal import HealthIndicatorsComparisonAPIView

from .health.viewindicatorproject import IndicadoresSaludPorProyectoView
from .health.viewindicatorscorrelation import CorrelationView

from .habits.viewhabitsbyuser import HabitosAPIView
from .habits.viewdatesofuser import GetDatesByIdView
from .viewusersproject import UsersProjectView
from .habits.viewhabitsbyuserall import UserHabitsAllAPIView

#autenticacion
from django.urls import path
from .views import RegistroUsuarioView, LoginUsuarioView, LogoutUsuarioView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView

from django.urls import path
from rest_framework.routers import DefaultRouter

from api.habits.viewhabitspatient import  RegistroHabitosView, ReporteAguaView, ReporteAireView, ReporteEjercicioPorcentajeView, ReporteEjercicioTipoView, ReporteEjercicioView, ReporteEsperanzaPorcentajeView, ReporteHorasDormidasView, ReportePorcentajeDescansoView, ReporteSolView
from .views import (
    RoleViewSet, UsuarioViewSet, DatosPersonalesUsuarioViewSet, AlimentacionViewSet, AguaViewSet, EsperanzaViewSet, 
    SolViewSet, AireViewSet, DormirViewSet, DespertarViewSet, EjercicioViewSet, ProyectoViewSet, UsuarioProyectoViewSet, DatosCorporalesViewSet, DatosHabitosViewSet
)
from .health.viewindicatorhealthy import IndicadoresSaludPorUsuarioView
from .health.viewindicatormainwithfinal import HealthIndicatorsComparisonAPIView

from .health.viewindicatorproject import IndicadoresSaludPorProyectoView
from .health.viewindicatorscorrelation import CorrelationView

from .habits.viewhabitsbyuser import HabitosAPIView
from .habits.viewdatesofuser import GetDatesByIdView
from .viewusersproject import UsersProjectView

from .habits.viewhabitsbyuserall import UserHabitsAllAPIView


router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'usuarios-personales', DatosPersonalesUsuarioViewSet)
router.register(r'alimentaciones', AlimentacionViewSet)
router.register(r'aguas', AguaViewSet)
router.register(r'esperanzas', EsperanzaViewSet)
router.register(r'soles', SolViewSet)
router.register(r'aires', AireViewSet)
router.register(r'sleeps', DormirViewSet)
router.register(r'despertares', DespertarViewSet)
router.register(r'ejercicios', EjercicioViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'usuario-proyectos', UsuarioProyectoViewSet)
router.register(r'datos-corporales', DatosCorporalesViewSet)
router.register(r'datos-habitos', DatosHabitosViewSet)

urlpatterns = [

    # estado del paciente
    path('indicadores-salud-por-usuario/<int:usuario_id>/', IndicadoresSaludPorUsuarioView.as_view(), name='indicadores_salud'),


    path('correlations-health-habits/', CorrelationView.as_view(), name='correlations-health-habits'),

    
    # estado del paciente segun el proyecto
    path('indicadores-salud-por-proyectos/<int:proyecto_id>/', IndicadoresSaludPorProyectoView.as_view(), name='proyecto-detalle'),

    ## Seccion seguimiento Usuarios
    #comparadores iniciales vs finales
    path('indicadores-salud-iniciales-finales/<int:usuario_id>/', HealthIndicatorsComparisonAPIView.as_view(), name='indicadores_salud'),


    #habitos entre fechas
    path('indicadores-habitos-por-usuario/<int:usuario_id>/', HabitosAPIView.as_view(), name='indicador-de-habito'),

   # Seccion seguimiento Usuarios
    #todos sus habitos
    path('indicadores-habitos-por-usuario-seguimiento/<int:usuario_id>/', UserHabitsAllAPIView.as_view(), name='todos-los-indicadores'),

    #usuarios de un proyecto
    path('usuarios-de-proyecto/<int:proyecto_id>/', UsersProjectView.as_view(), name='usuarios-proyecto'),
    path('fechas-min-max/<int:usuario_id>/', GetDatesByIdView.as_view(), name='fechas'),
        # Autenticación JWT
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    ##################################3 JUan
    ###########################     REPOSTES DE HABITOS PARA APP MOVIL  #############################################

    # Reporte de Agua por Usuarios la cantida de agua ingerida de cada dia durante la semana
    path('reporte-agua/<int:usuario_id>/', ReporteAguaView.as_view(), name='reporte-agua'),

    # Reporte de Aire por Usuarios el tiempo de aire que respiro de cada dia durante la semana
    path('reporte-aire/<int:usuario_id>/', ReporteAireView.as_view(), name='reporte-aire'),

    # Reporte de Ejercicio por Usuarios el tiempo de ejercicio de cada dia durante la semana
    path('reporte-ejercicio/<int:usuario_id>/', ReporteEjercicioView.as_view(), name='reporte-ejercicio'),
    # Porcentaje de cada tipo de ejercicio
    path('reporte-ejercicio-porcentaje/<int:usuario_id>/', ReporteEjercicioPorcentajeView.as_view(), name='reporte-ejercicio-porcentaje'),
    # # Reporte de Ejercicio por Usuarios y Tipo el tiempo de ejercicio de cada dia durante la semana
    path('reporte-ejercicio-tipo/<int:usuario_id>/<tipo_ejercicio>/', ReporteEjercicioTipoView.as_view(), name='reporte-ejercicio-tipo'),

    # Reporte de Aire el porcentaje de cata tipo
    path('reporte-esperanza/<int:usuario_id>/', ReporteEsperanzaPorcentajeView.as_view(), name='reporte-esperanza'),

    # Reporte de Sol por Usuarios la cantida de sol tomada de cada dia durante la semana
    path('reporte-sol/<int:usuario_id>/', ReporteSolView.as_view(), name='reporte-sol'),

    # Reporte de Descanso por Usuarios la cantida de horas dormidas de cada dia durante la semana
    path('reporte-descanso/<int:usuario_id>/', ReporteHorasDormidasView.as_view(), name='reporte-descanso'),
    # Porcentaje de estado por usuario de como descanso
    path('reporte-descanso-porcentaje/<int:usuario_id>/', ReportePorcentajeDescansoView.as_view(), name='reporte-descanso-porcentaje'),

    # Reporte general de registros de habitos de cada persona por dia
    path('registros-diarios/', RegistroHabitosView.as_view(), name='registros-diarios'),


]

urlpatterns += router.urls
