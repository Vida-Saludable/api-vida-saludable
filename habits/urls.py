from django.urls import path, include
from rest_framework.routers import DefaultRouter

from habits.views.datos_habitos_agua_view import DatosHabitosAguaViewSet, ListaDatosHabitosAguaUsuarioView
from habits.views.datos_habitos_aire_view import DatosHabitosAireViewSet, ListaDatosHabitosAireUsuarioView
from habits.views.datos_habitos_alimentacion_view import DatosHabitosAlimentacionViewSet, ListaDatosHabitosAlimentacionUsuarioView
from habits.views.datos_habitos_descanso_view import DatosHabitosDescansoViewSet, ListaDatosHabitosDescansoUsuarioView
from habits.views.datos_habitos_ejercicio_view import DatosHabitosEjercicioViewSet, ListaDatosHabitosEjercicioUsuarioView
from habits.views.datos_habitos_esperanza_view import DatosHabitosEsperanzaViewSet, ListaDatosHabitosEsperanzaUsuarioView
from habits.views.datos_habitos_sol_view import DatosHabitosSolViewSet, ListaDatosHabitosSolUsuarioView
from habits.views.datos_habitos_temperancia_view import DatosHabitosTemperanciaViewSet, ListaDatosHabitosTemperanciaUsuarioView

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
router.register(r'alimentaciones', AlimentacionViewSet)# listo
router.register(r'aguas', AguaViewSet)# listo
router.register(r'esperanzas', EsperanzaViewSet) #listo
router.register(r'soles', SolViewSet) #listo
router.register(r'aires', AireViewSet) #listo
router.register(r'sleeps', DormirViewSet) #listo
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
    path('datos-habitos-agua/usuario/<int:usuario_id>/', ListaDatosHabitosAguaUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-aire/usuario/<int:usuario_id>/', ListaDatosHabitosAireUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-alimentacion/usuario/<int:usuario_id>/', ListaDatosHabitosAlimentacionUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-ejercicio/usuario/<int:usuario_id>/', ListaDatosHabitosEjercicioUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-descanso/usuario/<int:usuario_id>/', ListaDatosHabitosDescansoUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-sol/usuario/<int:usuario_id>/', ListaDatosHabitosSolUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-temperancia/usuario/<int:usuario_id>/', ListaDatosHabitosTemperanciaUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
    path('datos-habitos-esperanza/usuario/<int:usuario_id>/', ListaDatosHabitosEsperanzaUsuarioView.as_view(), name='listar-datos-habitos-usuario'),
]

urlpatterns += router.urls