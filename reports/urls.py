from django.urls import path

from users.views.usuario_view import ListaUsuariosView

# from rest_framework.routers import DefaultRouter

from .views.reporte_aire_view import ReporteAireView
from .views.reporte_agua_view import ReporteAguaView
from .views.reporte_ejercicio_view import ReporteEjercicioView, ReporteEjercicioPorcentajeView, ReporteEjercicioTipoView
from .views.reporte_esperanza_view import ReporteEsperanzaPorcentajeView
from .views.reporte_sol_view import ReporteSolView
from .views.reporte_descanso_view import ReporteHorasDormidasView, ReportePorcentajeDescansoView
from .views.reporte_general_habitos_view import RegistroHabitosView

urlpatterns = [
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

    path('lista-usuarios/', ListaUsuariosView.as_view(), name='lista-usuarios'),


]

