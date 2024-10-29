from django.urls import path



from reports.views.cantidad_agua_excel_view import ClasificacionAguaUsuariosExcelAPIView
from reports.views.cantidad_agua_view import ClasificacionAguaUsuariosAPIView
from reports.views.cantidad_aire_excel_view import ClasificacionAireUsuariosExcelAPIView
from reports.views.cantidad_aire_view import ClasificacionAireUsuariosAPIView
from reports.views.cantidad_alimentos_excel_view import ClasificacionAlimentacionUsuariosExcelAPIView
from reports.views.cantidad_alimentos_view import ClasificacionAlimentacionUsuariosAPIView
from reports.views.cantidad_despertar_excel_view import ClasificacionDespertarUsuariosExcelAPIView
from reports.views.cantidad_despertar_view import ClasificacionDespertarUsuariosAPIView
from reports.views.cantidad_dormir_excel_view import ClasificacionDormirUsuariosExcelAPIView
from reports.views.cantidad_dormir_view import ClasificacionDormirUsuariosAPIView
from reports.views.cantidad_ejercicio_excel_view import ClasificacionEjercicioUsuariosExcelAPIView
from reports.views.cantidad_ejercicio_view import ClasificacionEjercicioUsuariosAPIView
from reports.views.cantidad_esperanza_excel_view import ClasificacionEsperanzaUsuariosExcelAPIView
from reports.views.cantidad_esperanza_view import ClasificacionEsperanzaUsuariosAPIView
from reports.views.cantidad_sol_excel_view import ClasificacionSolUsuariosExcelAPIView
from reports.views.cantidad_sol_view import ClasificacionSolUsuariosAPIView
from reports.views.cantidad_suenio_view import ClasificacionSuenioUsuariosAPIView
from reports.views.unicos_agua_view import AguaUnicosAPIView
from reports.views.unicos_aire_view import AireUnicosAPIView
from reports.views.unicos_alimentos_view import AlimentacionUnicosAPIView
from reports.views.unicos_despertar_view import DespertarUnicosAPIView
from reports.views.unicos_dormir_view import DormirUnicosAPIView
from reports.views.unicos_ejercicio_view import EjercicioUnicosAPIView
from reports.views.unicos_esperanza_view import EsperanzaUnicosAPIView
from reports.views.unicos_sol_view import SolUnicosAPIView







# from users.views.usuario_view import ListaUsuariosView

# from rest_framework.routers import DefaultRouter

from .views.reporte_aire_view import ReporteAireView
from .views.reporte_agua_view import ReporteAguaView
from .views.reporte_ejercicio_view import ReporteEjercicioView, ReporteEjercicioPorcentajeView, ReporteEjercicioTipoView
from .views.reporte_esperanza_view import ReporteEsperanzaPorcentajeView
from .views.reporte_sol_view import ReporteSolView
from .views.reporte_descanso_view import ReporteHorasDormidasView, ReportePorcentajeDescansoView
from reports.views.reporte_alimentacion_view import ReportePorcentajeAlimentacionTipoView, ReportePorcentajeAlimentacionView
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

    # Porcentaje de alimentacion comida saludable y no saludable
    path('reporte-alimentacion-porcentaje/<int:usuario_id>/', ReportePorcentajeAlimentacionView.as_view(), name='reporte-alimentacion-porcentaje'),
    # Porcentaje de alimentacion comida saludable y no saludable por tipo
    path('reporte-alimentacion-porcentaje-tipo/<int:usuario_id>/<str:tipo_alimento>/', ReportePorcentajeAlimentacionTipoView.as_view(), name='reporte-alimentacion-porcentaje-tipo'),

    # Reporte general de registros de habitos de cada persona por dia
    path('registros-diarios/', RegistroHabitosView.as_view(), name='registros-diarios'),


    
    
    
    
# Alimentación
    path('alimentacion-unicos/', AlimentacionUnicosAPIView.as_view(), name='alimentacion-unicos'),
    path('clasificacion-alimentacion-usuarios/', ClasificacionAlimentacionUsuariosAPIView.as_view(), name='clasificacion-alimentacion-usuarios'),
    path('clasificacion-alimentacion-usuarios-excel/', ClasificacionAlimentacionUsuariosExcelAPIView.as_view(), name='clasificacion-alimentacion-usuarios-excel'),


    # Agua
    path('agua-unicos/', AguaUnicosAPIView.as_view(), name='agua-unicos'),
    path('clasificacion-agua-usuarios/', ClasificacionAguaUsuariosAPIView.as_view(), name='clasificacion-agua-usuarios'),
    path('clasificacion-agua-usuarios-excel/', ClasificacionAguaUsuariosExcelAPIView.as_view(), name='clasificacion-agua-usuarios-excel'),

    # Aire
    path('aire-unicos/', AireUnicosAPIView.as_view(), name='aire-unicos'),
    path('clasificacion-aire-usuarios/', ClasificacionAireUsuariosAPIView.as_view(), name='clasificacion-aire-usuarios'),
    path('clasificacion-aire-usuarios-excel/', ClasificacionAireUsuariosExcelAPIView.as_view(), name='clasificacion-aire-usuarios-excel'),


    # Despertar
    path('despertar-unicos/', DespertarUnicosAPIView.as_view(), name='despertar-unicos'),
    path('clasificacion-despertar-usuarios/', ClasificacionDespertarUsuariosAPIView.as_view(), name='clasificacion-despertar-usuarios'),
    path('clasificacion-despertar-usuarios-excel/', ClasificacionDespertarUsuariosExcelAPIView.as_view(), name='clasificacion-despertar-usuarios-excel'),


    # Sueño (calculado con Dormir y Despertar)
    path('dormir-unicos/', DormirUnicosAPIView.as_view(), name='suenio-unicos'),
    path('clasificacion-dormir-usuarios/', ClasificacionDormirUsuariosAPIView.as_view(), name='clasificacion-suenio-usuarios'),
    path('clasificacion-dormir-usuarios-excel/', ClasificacionDormirUsuariosExcelAPIView.as_view(), name='clasificacion-dormir-usuarios-excel'),


    # Ejercicio
    path('ejercicio-unicos/', EjercicioUnicosAPIView.as_view(), name='ejercicio-unicos'),
    path('clasificacion-ejercicio-usuarios/', ClasificacionEjercicioUsuariosAPIView.as_view(), name='clasificacion-ejercicio-usuarios'),
    path('clasificacion-ejercicio-usuarios-excel/', ClasificacionEjercicioUsuariosExcelAPIView.as_view(), name='clasificacion-ejercicio-usuarios-excel'),


    # Esperanza
    path('esperanza-unicos/', EsperanzaUnicosAPIView.as_view(), name='esperanza-unicos'),
    path('clasificacion-esperanza-usuarios/', ClasificacionEsperanzaUsuariosAPIView.as_view(), name='clasificacion-esperanza-usuarios'),
    path('clasificacion-esperanza-usuarios-excel/', ClasificacionEsperanzaUsuariosExcelAPIView.as_view(), name='clasificacion-esperanza-usuarios-excel'),


    # Sol
    path('sol-unicos/', SolUnicosAPIView.as_view(), name='sol-unicos'),
    path('clasificacion-sol-usuarios/', ClasificacionSolUsuariosAPIView.as_view(), name='clasificacion-sol-usuarios'),
    path('clasificacion-sol-usuarios-excel/', ClasificacionSolUsuariosExcelAPIView.as_view(), name='clasificacion-sol-usuarios-excel'),




    

]

