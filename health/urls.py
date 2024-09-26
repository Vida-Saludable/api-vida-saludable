from django.urls import path

from health.views.correlationhabitsvshealthydeltas_view import CorrelationHealthyVsHabitsDeltas
from health.views.viewindicatorhealthy import IndicadoresSaludPorUsuarioView
from health.views.viewindicatormainwithfinal import HealthIndicatorsComparisonAPIView

from health.views.viewindicatorproject import IndicadoresSaludPorProyectoView
from health.views.viewindicatorscorrelation import CorrelationView

from health.views.viewhabitsbyuser import HabitosAPIView
from health.views.viewdatesofuser import GetDatesByIdView

from health.views.viewhabitsbyuserall import UserHabitsAllAPIView


urlpatterns = [
    path('indicadores-salud-por-usuario/<int:usuario_id>/', IndicadoresSaludPorUsuarioView.as_view(), name='indicadores_salud'),
    path('correlations-health-habits/', CorrelationView.as_view(), name='correlations-health-habits'),
    path('correlations-health-habits-deltas/', CorrelationHealthyVsHabitsDeltas.as_view(), name='correlations-health-habits-deltas'),
    path('indicadores-salud-por-proyectos/<int:proyecto_id>/', IndicadoresSaludPorProyectoView.as_view(), name='proyecto-detalle'),
    path('indicadores-salud-iniciales-finales/<int:usuario_id>/', HealthIndicatorsComparisonAPIView.as_view(), name='indicadores_salud'),
    path('indicadores-habitos-por-usuario/<int:usuario_id>/', HabitosAPIView.as_view(), name='indicador-de-habito'),
    path('indicadores-habitos-por-usuario-seguimiento/<int:usuario_id>/', UserHabitsAllAPIView.as_view(), name='todos-los-indicadores'),
    path('fechas-min-max/<int:usuario_id>/', GetDatesByIdView.as_view(), name='fechas'),
]
