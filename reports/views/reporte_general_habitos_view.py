from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Max, Func
from rest_framework.pagination import PageNumberPagination

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

class Round(Func):
    function = 'ROUND'
class RegistroHabitosPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegistroHabitosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            resultado_agrupado = defaultdict(lambda: defaultdict(dict))
            paginator = RegistroHabitosPagination()

            # Obtener parámetros de búsqueda y paginación
            nombre = request.query_params.get('nombre', None)
            proyecto_id = request.query_params.get('proyecto', None)
            fecha_inicial = request.query_params.get('fecha_inicial', None)
            fecha_final = request.query_params.get('fecha_final', None)

            # Validar y convertir fechas
            date_filters = {}
            if fecha_inicial:
                try:
                    date_filters['fecha__gte'] = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
                except ValueError:
                    return Response(
                        {'error': 'Formato de fecha_inicial inválido. Use YYYY-MM-DD'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if fecha_final:
                try:
                    date_filters['fecha__lte'] = datetime.strptime(fecha_final, '%Y-%m-%d').date()
                except ValueError:
                    return Response(
                        {'error': 'Formato de fecha_final inválido. Use YYYY-MM-DD'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Primero, obtener los IDs de usuarios filtrados
            usuarios_filtrados = Usuario.objects.all()
            
            if nombre:
                usuarios_filtrados = usuarios_filtrados.filter(
                    datospersonalesusuario__nombres_apellidos__icontains=nombre
                )
            
            if proyecto_id:
                usuarios_filtrados = usuarios_filtrados.filter(
                    usuarioproyecto__proyecto_id=proyecto_id
                )
            
            usuarios_ids = usuarios_filtrados.values_list('id', flat=True)

            # Consulta de alimentación con filtros aplicados
            registros_alimentacion = Alimentacion.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'usuario_id').annotate(
                desayuno=Sum('desayuno'),
                almuerzo=Sum('almuerzo'),
                cena=Sum('cena')
            )
            
            for registro in registros_alimentacion:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'alimentacion' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['alimentacion'] = {}
                resultado_agrupado[usuario_id][fecha]['alimentacion'].update({
                    'desayuno': registro['desayuno'],
                    'almuerzo': registro['almuerzo'],
                    'cena': registro['cena'],
                })

            # Consulta de aire con filtros
            registros_aire = Aire.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            
            for registro in registros_aire:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'aire' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['aire'] = {}
                resultado_agrupado[usuario_id][fecha]['aire'].update({'tiempo': registro['tiempo']})

            # Consulta de agua con filtros
            registros_agua = Agua.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'usuario_id').annotate(
                cantidad=Sum('cantidad')
            )
            
            for registro in registros_agua:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'agua' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['agua'] = {}
                resultado_agrupado[usuario_id][fecha]['agua'].update({'cantidad': registro['cantidad']})

            # Consulta de ejercicio con filtros
            registros_ejercicio = Ejercicio.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'tipo', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            
            for registro in registros_ejercicio:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'ejercicio' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['ejercicio'] = []
                resultado_agrupado[usuario_id][fecha]['ejercicio'].append({
                    'tipo': registro['tipo'],
                    'tiempo': registro['tiempo']
                })

            # Consulta de esperanza con filtros
            registros_esperanza = Esperanza.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'tipo_practica', 'usuario_id')
            
            for registro in registros_esperanza:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'esperanza' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['esperanza'] = []
                resultado_agrupado[usuario_id][fecha]['esperanza'].append({
                    'tipo_practica': registro['tipo_practica']
                })

            # Consulta de sol con filtros
            registros_sol = Sol.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            
            for registro in registros_sol:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'sol' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['sol'] = {}
                resultado_agrupado[usuario_id][fecha]['sol'].update({'tiempo': registro['tiempo']})

            # Consulta de dormir y despertar con filtros
            registros_dormir = Dormir.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'hora', 'usuario_id')
            
            registros_despertar = Despertar.objects.filter(
                usuario_id__in=usuarios_ids,
                **date_filters
            ).values('fecha', 'hora', 'usuario_id', 'estado')

            for dormir in registros_dormir:
                usuario_id = dormir['usuario_id']
                fecha_dormir = dormir['fecha']
                despertar = registros_despertar.filter(
                    usuario_id=usuario_id,
                    fecha=dormir['fecha'],
                    hora__gte=dormir['hora']
                ).order_by('hora').first()

                if not despertar:
                    despertar = registros_despertar.filter(
                        usuario_id=usuario_id,
                        fecha=dormir['fecha'] + timedelta(days=1),
                        hora__lt=dormir['hora']
                    ).order_by('hora').first()

                if despertar:
                    hora_dormir = datetime.combine(dormir['fecha'], dormir['hora'])
                    hora_despertar = datetime.combine(despertar['fecha'], despertar['hora'])

                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)

                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    total_horas = tiempo_dormido // 3600
                    total_minutos = (tiempo_dormido % 3600) // 60

                    if 'descanso' not in resultado_agrupado[usuario_id][fecha_dormir]:
                        resultado_agrupado[usuario_id][fecha_dormir]['descanso'] = {
                            'total_horas': 0,
                            'total_minutos': 0
                        }

                    resultado_agrupado[usuario_id][fecha_dormir]['descanso']['total_horas'] += int(total_horas)
                    resultado_agrupado[usuario_id][fecha_dormir]['descanso']['total_minutos'] += int(total_minutos)

            # Obtener datos personales solo para usuarios filtrados
            datos_personales = DatosPersonalesUsuario.objects.filter(
                usuario__id__in=usuarios_ids
            ).values('usuario_id', 'nombres_apellidos', 'telefono')

            # Obtener el peso más reciente de cada usuario
            pesos_recientes = DatosFisicos.objects.filter(
                usuario_id__in=usuarios_ids
            ).values('usuario_id').annotate(
                peso_reciente=Max('fecha')
            ).values('usuario_id', 'peso', 'fecha')
    
            # Crear un diccionario con el peso más reciente por usuario
            pesos_dict = {peso['usuario_id']: peso['peso'] for peso in pesos_recientes}

            datos_personales_dict = {
                datos['usuario_id']: {
                    'nombres_apellidos': datos['nombres_apellidos'],
                    'telefono': datos['telefono'],
                    'peso': pesos_dict.get(datos['usuario_id'], None)
                } for datos in datos_personales
            }

            # Obtener proyectos solo para usuarios filtrados
            proyectos_usuario = UsuarioProyecto.objects.filter(
                usuario__id__in=usuarios_ids
            ).select_related('proyecto')

            proyectos_dict = defaultdict(list)
            for proyecto in proyectos_usuario:
                proyectos_dict[proyecto.usuario_id].append(proyecto.proyecto.nombre)

            # Formatear los resultados finales
            resultado_final = []
            for usuario_id, fechas in resultado_agrupado.items():
                for fecha, datos in fechas.items():
                    # Inicializar datos a 0 si no existen
                    if 'alimentacion' not in datos:
                        datos['alimentacion'] = {'desayuno': 0, 'almuerzo': 0, 'cena': 0}
                    else:
                        datos['alimentacion']['desayuno'] = datos['alimentacion'].get('desayuno', 0) or 0
                        datos['alimentacion']['almuerzo'] = datos['alimentacion'].get('almuerzo', 0) or 0
                        datos['alimentacion']['cena'] = datos['alimentacion'].get('cena', 0) or 0

                    if 'aire' not in datos:
                        datos['aire'] = {'tiempo': 0}
                    else:
                        datos['aire']['tiempo'] = datos['aire'].get('tiempo', 0) or 0

                    if 'agua' not in datos:
                        datos['agua'] = {'cantidad': 0}
                    else:
                        datos['agua']['cantidad'] = datos['agua'].get('cantidad', 0) or 0

                    if 'ejercicio' not in datos:
                        datos['ejercicio'] = []
                    if 'esperanza' not in datos:
                        datos['esperanza'] = []
                    if 'sol' not in datos:
                        datos['sol'] = {'tiempo': 0}
                    else:
                        datos['sol']['tiempo'] = datos['sol'].get('tiempo', 0) or 0

                    if 'descanso' not in datos:
                        datos['descanso'] = {'total_horas': 0, 'total_minutos': 0}

                    datos_finales = {
                        'fecha': fecha,
                        'usuario': datos_personales_dict.get(usuario_id, {}),
                        'alimentacion': datos['alimentacion'],
                        'aire': datos['aire'],
                        'agua': datos['agua'],
                        'ejercicio': datos['ejercicio'],
                        'esperanza': datos['esperanza'],
                        'sol': datos['sol'],
                        'descanso': datos['descanso'],
                        'proyectos': proyectos_dict[usuario_id],
                    }
                    resultado_final.append(datos_finales)

            # Aplicar paginación
            paginated_result = paginator.paginate_queryset(resultado_final, request)

            response_data = {
                'success': True,
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'data': paginated_result
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)