from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habits.views.datos_habitos_agua_view import DatosHabitosAguaViewSet
from habits.views.datos_habitos_aire_view import DatosHabitosAireViewSet
from habits.views.datos_habitos_alimentacion_view import DatosHabitosAlimentacionViewSet
from habits.views.datos_habitos_descanso_view import DatosHabitosDescansoViewSet
from habits.views.datos_habitos_ejercicio_view import DatosHabitosEjercicioViewSet
from habits.views.datos_habitos_esperanza_view import DatosHabitosEsperanzaViewSet
from habits.views.datos_habitos_sol_view import DatosHabitosSolViewSet
from habits.views.datos_habitos_temperancia_view import DatosHabitosTemperanciaViewSet

from .views.agua_view import AguaViewSet
from .views.aire_view import AireViewSet
from .views.alimentacion_view import AlimentacionViewSet
from .views.sol_view import SolViewSet
from .views.esperanza_view import EsperanzaViewSet
from .views.dormir_view import DormirViewSet
from .views.despertar_view import DespertarViewSet
from .views.ejercicio_view import EjercicioViewSet
# from .views.datos_habitos_view import DatosHabitosViewSet

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
router.register(r'datos-habitos-agua', DatosHabitosAguaViewSet)
router.register(r'datos-habitos-aire', DatosHabitosAireViewSet)
router.register(r'datos-habitos-alimentacion', DatosHabitosAlimentacionViewSet)
router.register(r'datos-habitos-ejercicio', DatosHabitosEjercicioViewSet)
router.register(r'datos-habitos-descanso', DatosHabitosDescansoViewSet)
router.register(r'datos-habitos-sol', DatosHabitosSolViewSet)
router.register(r'datos-habitos-temperancia', DatosHabitosTemperanciaViewSet)
router.register(r'datos-habitos-esperanza', DatosHabitosEsperanzaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
