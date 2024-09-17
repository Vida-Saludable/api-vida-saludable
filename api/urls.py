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

]

urlpatterns += router.urls
