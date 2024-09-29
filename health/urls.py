from django.urls import path
from rest_framework.routers import DefaultRouter

from health.views.correlationhabitsvshealthydeltas_view import CorrelationHealthyVsHabitsDeltas
from health.views.datos_fisicos_view import DatosFisicosViewSet
from health.views.datos_muestras_view import DatosMuestrasViewSet
from health.views.signos_vitales_view import SignosVitalesViewSet
from health.views.test_ruffier_view import TestRuffierViewSet
from health.views.viewindicatorhealthy import IndicadoresSaludPorUsuarioView
from health.views.viewindicatormainwithfinal import HealthIndicatorsComparisonAPIView

from health.views.viewindicatorproject import IndicadoresSaludPorProyectoView
from health.views.viewindicatorscorrelation import CorrelationView

from health.views.typecorrelation_view import TiposDeCorrelacionView

from health.views.viewhabitsbyuser import HabitosAPIView
from health.views.viewdatesofuser import GetDatesByIdView

from health.views.viewhabitsbyuserall import UserHabitsAllAPIView

# Crea un enrutador para la aplicación users
router = DefaultRouter()
router.register(r'datos-fisicos', DatosFisicosViewSet)
router.register(r'datos-muestras', DatosMuestrasViewSet)
router.register(r'signos-vitales', SignosVitalesViewSet)
router.register(r'test-ruffier', TestRuffierViewSet)


urlpatterns = [
    path('indicadores-salud-por-usuario/<int:usuario_id>/', IndicadoresSaludPorUsuarioView.as_view(), name='indicadores_salud'),
    path('correlations-health-habits/', CorrelationView.as_view(), name='correlations-health-habits'),
    path('correlations-health-habits-deltas/', CorrelationHealthyVsHabitsDeltas.as_view(), name='correlations-health-habits-deltas'),
    path('indicadores-salud-por-proyectos/<int:proyecto_id>/', IndicadoresSaludPorProyectoView.as_view(), name='proyecto-detalle'),
    path('indicadores-salud-iniciales-finales/<int:usuario_id>/', HealthIndicatorsComparisonAPIView.as_view(), name='indicadores_salud'),
    path('indicadores-habitos-por-usuario/<int:usuario_id>/', HabitosAPIView.as_view(), name='indicador-de-habito'),
    path('indicadores-habitos-por-usuario-seguimiento/<int:usuario_id>/', UserHabitsAllAPIView.as_view(), name='todos-los-indicadores'),
    path('fechas-min-max/<int:usuario_id>/', GetDatesByIdView.as_view(), name='fechas'),
    path('tipos-correlacion/', TiposDeCorrelacionView.as_view(), name='tipos-correlacion'),
]

urlpatterns += router.urls