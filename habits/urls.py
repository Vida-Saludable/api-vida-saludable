from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.agua_view import AguaViewSet
from .views.aire_view import AireViewSet
from .views.alimentacion_view import AlimentacionViewSet
from .views.sol_view import SolViewSet
from .views.esperanza_view import EsperanzaViewSet
from .views.dormir_view import DormirViewSet
from .views.despertar_view import DespertarViewSet
from .views.ejercicio_view import EjercicioViewSet
from .views.datos_habitos_view import DatosHabitosViewSet

# Crea un enrutador para la aplicación habits
router = DefaultRouter()
router.register(r'alimentaciones', AlimentacionViewSet)
router.register(r'aguas', AguaViewSet)
router.register(r'esperanzas', EsperanzaViewSet)
router.register(r'soles', SolViewSet)
router.register(r'aires', AireViewSet)
router.register(r'sleeps', DormirViewSet)
router.register(r'despertares', DespertarViewSet)
router.register(r'ejercicios', EjercicioViewSet)
router.register(r'datos-habitos', DatosHabitosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
