from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.http import HttpResponse
from django.db.models import Sum, Max
import pandas as pd

from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from health.models.datos_fisicos_models import DatosFisicos
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from habits.models.alimentacion_model import Alimentacion
from habits.models.esperanza_model import Esperanza
from habits.models.ejercicio_model import Ejercicio
from habits.models.aire_model import Aire
from habits.models.agua_model import Agua
from habits.models.sol_model import Sol
from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto


class ExportarHabitosExcelView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            resultado_agrupado = defaultdict(lambda: defaultdict(dict))

            # Obtener filtros
            nombre = request.query_params.get('nombre', None)
            proyecto_id = request.query_params.get('proyecto', None)
            fecha_inicial = request.query_params.get('fecha_inicial', None)
            fecha_final = request.query_params.get('fecha_final', None)

            date_filters = {}
            if fecha_inicial:
                date_filters['fecha__gte'] = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
            if fecha_final:
                date_filters['fecha__lte'] = datetime.strptime(fecha_final, '%Y-%m-%d').date()

            usuarios_filtrados = Usuario.objects.all()
            if nombre:
                usuarios_filtrados = usuarios_filtrados.filter(datospersonalesusuario__nombres_apellidos__icontains=nombre)
            if proyecto_id:
                usuarios_filtrados = usuarios_filtrados.filter(usuarioproyecto__proyecto_id=proyecto_id)

            usuarios_ids = usuarios_filtrados.values_list('id', flat=True)

            registros_alimentacion = Alimentacion.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'usuario_id').annotate(
                desayuno=Sum('desayuno'), almuerzo=Sum('almuerzo'), cena=Sum('cena')
            )
            for r in registros_alimentacion:
                resultado_agrupado[r['usuario_id']][r['fecha']]['alimentacion'] = {
                    'desayuno': r['desayuno'], 'almuerzo': r['almuerzo'], 'cena': r['cena']
                }

            registros_aire = Aire.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for r in registros_aire:
                resultado_agrupado[r['usuario_id']][r['fecha']]['aire'] = {'tiempo': r['tiempo']}

            registros_agua = Agua.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'usuario_id').annotate(
                cantidad=Sum('cantidad')
            )
            for r in registros_agua:
                resultado_agrupado[r['usuario_id']][r['fecha']]['agua'] = {'cantidad': r['cantidad']}

            registros_sol = Sol.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for r in registros_sol:
                resultado_agrupado[r['usuario_id']][r['fecha']]['sol'] = {'tiempo': r['tiempo']}

            registros_ejercicio = Ejercicio.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'tipo', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for r in registros_ejercicio:
                resultado_agrupado[r['usuario_id']][r['fecha']].setdefault('ejercicio', []).append({
                    'tipo': r['tipo'], 'tiempo': r['tiempo']
                })

            registros_esperanza = Esperanza.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'tipo_practica', 'usuario_id')
            for r in registros_esperanza:
                resultado_agrupado[r['usuario_id']][r['fecha']].setdefault('esperanza', []).append({
                    'tipo_practica': r['tipo_practica']
                })

            registros_dormir = Dormir.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'hora', 'usuario_id')
            registros_despertar = Despertar.objects.filter(usuario_id__in=usuarios_ids, **date_filters).values('fecha', 'hora', 'usuario_id')

            for dormir in registros_dormir:
                usuario_id = dormir['usuario_id']
                fecha_dormir = dormir['fecha']
                hora_dormir = datetime.combine(dormir['fecha'], dormir['hora'])
                despertar = next((d for d in registros_despertar if d['usuario_id'] == usuario_id and d['fecha'] >= fecha_dormir), None)
                if despertar:
                    hora_despertar = datetime.combine(despertar['fecha'], despertar['hora'])
                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)
                    duracion = hora_despertar - hora_dormir
                    total_horas = duracion.total_seconds() // 3600
                    total_minutos = (duracion.total_seconds() % 3600) // 60
                    resultado_agrupado[usuario_id][fecha_dormir]['descanso'] = {
                        'total_horas': int(total_horas),
                        'total_minutos': int(total_minutos)
                    }

            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id__in=usuarios_ids).values(
                'usuario_id', 'nombres_apellidos', 'telefono'
            )
            datos_personales_dict = {d['usuario_id']: d for d in datos_personales}

            proyectos = UsuarioProyecto.objects.filter(usuario_id__in=usuarios_ids).select_related('proyecto')
            proyectos_dict = defaultdict(list)
            for p in proyectos:
                proyectos_dict[p.usuario_id].append(p.proyecto.nombre)

            resultado_final = []
            for usuario_id, fechas in resultado_agrupado.items():
                for fecha, datos in fechas.items():
                    datos_finales = {
                        'fecha': fecha,
                        'usuario': datos_personales_dict.get(usuario_id, {}).get('nombres_apellidos', ''),
                        'telefono': datos_personales_dict.get(usuario_id, {}).get('telefono', ''),
                        'proyectos': ", ".join(proyectos_dict[usuario_id]),
                        'desayuno': datos.get('alimentacion', {}).get('desayuno', 0),
                        'almuerzo': datos.get('alimentacion', {}).get('almuerzo', 0),
                        'cena': datos.get('alimentacion', {}).get('cena', 0),
                        'agua': datos.get('agua', {}).get('cantidad', 0),
                        'aire': datos.get('aire', {}).get('tiempo', 0),
                        'sol': datos.get('sol', {}).get('tiempo', 0),
                        'ejercicio': "; ".join([f"{e['tipo']} ({e['tiempo']} min)" for e in datos.get('ejercicio', [])]),
                        'esperanza': "; ".join([e['tipo_practica'] for e in datos.get('esperanza', [])]),
                        'horas_dormidas': datos.get('descanso', {}).get('total_horas', 0),
                        'minutos_dormidos': datos.get('descanso', {}).get('total_minutos', 0),
                    }
                    resultado_final.append(datos_finales)

            df = pd.DataFrame(resultado_final)
            fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M')
            nombre = request.query_params.get('nombre', 'general')
            proyecto = request.query_params.get('proyecto', 'todos')
            nombre_archivo = f"registro_habitos_{nombre}_{proyecto}_{fecha_actual}.xlsx".replace(' ', '_')

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Reporte', index=False)

            return response

        except Exception as e:
            return HttpResponse(f"Error al generar el Excel: {str(e)}", status=500)

class ExportarAireExcelView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            proyecto_id = request.query_params.get('proyecto', None)
            fecha_inicial = request.query_params.get('fecha_inicial', None)
            fecha_final = request.query_params.get('fecha_final', None)

            date_filters = {}
            if fecha_inicial:
                date_filters['fecha__gte'] = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
            if fecha_final:
                date_filters['fecha__lte'] = datetime.strptime(fecha_final, '%Y-%m-%d').date()

            usuarios_filtrados = Usuario.objects.all()
            if proyecto_id:
                usuarios_filtrados = usuarios_filtrados.filter(usuarioproyecto__proyecto_id=proyecto_id)

            usuarios_ids = usuarios_filtrados.values_list('id', flat=True)

            registros_aire = Aire.objects.filter(usuario_id__in=usuarios_ids, **date_filters)

            proyectos = UsuarioProyecto.objects.filter(usuario_id__in=usuarios_ids).select_related('proyecto')
            proyectos_dict = defaultdict(list)
            for p in proyectos:
                proyectos_dict[p.usuario_id].append(p.proyecto.nombre)

            resultado_final = []
            for r in registros_aire:
                resultado_final.append({
                    'id': r.id,
                    'fecha': r.fecha,
                    'tiempo': r.tiempo,
                    'usuario_id': r.usuario_id,
                    'proyectos': ", ".join(proyectos_dict[r.usuario_id])
                })

            df = pd.DataFrame(resultado_final)
            fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M')
            nombre_archivo = f"aire_export_{fecha_actual}.xlsx"

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Aire', index=False)

            return response

        except Exception as e:
            return HttpResponse(f"Error al generar el Excel: {str(e)}", status=500)
