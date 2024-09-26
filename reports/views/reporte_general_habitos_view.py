from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

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


class RegistroHabitosView(APIView):
    def get(self, request):
        try:
            resultado_agrupado = defaultdict(lambda: defaultdict(dict))

            # Consulta de alimentación
            registros_alimentacion = Alimentacion.objects.values('fecha', 'usuario_id').annotate(
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

            # Consulta de aire
            registros_aire = Aire.objects.values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for registro in registros_aire:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'aire' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['aire'] = {}
                resultado_agrupado[usuario_id][fecha]['aire'].update({'tiempo': registro['tiempo']})

            # Consulta de agua
            registros_agua = Agua.objects.values('fecha', 'usuario_id').annotate(
                cantidad=Sum('cantidad')
            )
            for registro in registros_agua:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'agua' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['agua'] = {}
                resultado_agrupado[usuario_id][fecha]['agua'].update({'cantidad': registro['cantidad']})

            # Consulta de ejercicio
            registros_ejercicio = Ejercicio.objects.values('fecha', 'tipo', 'usuario_id').annotate(
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

            # Consulta de esperanza
            registros_esperanza = Esperanza.objects.values('fecha', 'tipo_practica', 'usuario_id')
            for registro in registros_esperanza:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'esperanza' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['esperanza'] = []
                resultado_agrupado[usuario_id][fecha]['esperanza'].append({
                    'tipo_practica': registro['tipo_practica']
                })

            # Consulta de sol
            registros_sol = Sol.objects.values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for registro in registros_sol:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'sol' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['sol'] = {}
                resultado_agrupado[usuario_id][fecha]['sol'].update({'tiempo': registro['tiempo']})

            # Consulta de dormir y despertar
            registros_dormir = Dormir.objects.values('fecha', 'hora', 'usuario_id')
            registros_despertar = Despertar.objects.values('fecha', 'hora', 'usuario_id', 'estado')

            for dormir in registros_dormir:
                usuario_id = dormir['usuario_id']
                fecha_dormir = dormir['fecha']
                despertar = registros_despertar.filter(
                    fecha=dormir['fecha'],
                    hora__gte=dormir['hora']
                ).order_by('hora').first()

                if not despertar:
                    despertar = registros_despertar.filter(
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

            # Obtener todos los usuarios
            todos_usuarios = Usuario.objects.all().values('id')

            # Inicializar resultados para usuarios sin registros
            for usuario in todos_usuarios:
                usuario_id = usuario['id']
                if usuario_id not in resultado_agrupado:
                    resultado_agrupado[usuario_id] = defaultdict(dict)

            datos_personales = DatosPersonalesUsuario.objects.filter(usuario__id__in=resultado_agrupado.keys()).values('usuario_id', 'nombres_apellidos', 'telefono')

            datos_personales_dict = {datos['usuario_id']: {'nombres_apellidos': datos['nombres_apellidos'], 'telefono': datos['telefono']} for datos in datos_personales}

            # Asociar los proyectos a cada usuario
            proyectos_usuario = UsuarioProyecto.objects.filter(usuario__id__in=resultado_agrupado.keys()).select_related('proyecto')

            proyectos_dict = defaultdict(list)
            for proyecto in proyectos_usuario:
                proyectos_dict[proyecto.usuario_id].append(proyecto.proyecto.nombre)

            # Formatear los resultados finales
            resultado_final = []
            for usuario_id, fechas in resultado_agrupado.items():
                for fecha, datos in fechas.items():
                    # Inicializar datos a nulos si no existen
                    if 'alimentacion' not in datos:
                        datos['alimentacion'] = {'desayuno': None, 'almuerzo': None, 'cena': None}
                    if 'aire' not in datos:
                        datos['aire'] = {'tiempo': None}
                    if 'agua' not in datos:
                        datos['agua'] = {'cantidad': None}
                    if 'ejercicio' not in datos:
                        datos['ejercicio'] = []
                    if 'esperanza' not in datos:
                        datos['esperanza'] = []
                    if 'sol' not in datos:
                        datos['sol'] = {'tiempo': None}
                    if 'descanso' not in datos:
                        datos['descanso'] = {'total_horas': 0, 'total_minutos': 0}

                    # Agregar datos del usuario
                    datos_usuario = datos_personales_dict.get(usuario_id, {})
                    datos['usuario'] = datos_usuario

                    # Agregar proyectos asociados al usuario
                    datos['proyectos'] = proyectos_dict.get(usuario_id, [])

                    resultado_final.append({
                        'fecha': fecha,
                        'usuario': datos_usuario,
                        **datos
                    })

            return Response({
                "success": True,
                "message": "Datos recuperados con éxito.",
                "data": resultado_final
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

