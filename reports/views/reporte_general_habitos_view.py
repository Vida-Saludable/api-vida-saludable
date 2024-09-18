from collections import defaultdict
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

from ...users.models.datos_personales_usuario_model import DatosPersonalesUsuario

from ...habits.models.dormir_model import Dormir
from ...habits.models.despertar_model import Despertar
from ...habits.models.alimentacion_model import Alimentacion
from ...habits.models.esperanza_model import Esperanza
from ...habits.models.ejercicio_model import Ejercicio
from ...habits.models.aire_model import Aire
from ...habits.models.agua_model import Agua
from ...habits.models.sol_model import Sol


class RegistroHabitosView(APIView):
    def get(self, request):
        try:
            # Diccionario para agrupar los datos por usuario y fecha
            resultado_agrupado = defaultdict(lambda: defaultdict(dict))

            # Registros de alimentación (Desayuno, Almuerzo, Cena)
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

            # Registros de Aire (suma de tiempo por fecha)
            registros_aire = Aire.objects.values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for registro in registros_aire:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'aire' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['aire'] = {}
                resultado_agrupado[usuario_id][fecha]['aire'].update({'tiempo': registro['tiempo']})

            # Registros de Agua (suma de cantidad por fecha)
            registros_agua = Agua.objects.values('fecha', 'usuario_id').annotate(
                cantidad=Sum('cantidad')
            )
            for registro in registros_agua:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'agua' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['agua'] = {}
                resultado_agrupado[usuario_id][fecha]['agua'].update({'cantidad': registro['cantidad']})

            # Registros de Ejercicio (suma de tiempo por tipo de ejercicio y fecha)
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

            # Registros de Esperanza (se devuelven los registros por tipo_practica)
            registros_esperanza = Esperanza.objects.values('fecha', 'tipo_practica', 'usuario_id')
            for registro in registros_esperanza:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'esperanza' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['esperanza'] = []
                resultado_agrupado[usuario_id][fecha]['esperanza'].append({
                    'tipo_practica': registro['tipo_practica']
                })

            # Registros de Sol (suma de tiempo por fecha)
            registros_sol = Sol.objects.values('fecha', 'usuario_id').annotate(
                tiempo=Sum('tiempo')
            )
            for registro in registros_sol:
                usuario_id = registro['usuario_id']
                fecha = registro['fecha']
                if 'sol' not in resultado_agrupado[usuario_id][fecha]:
                    resultado_agrupado[usuario_id][fecha]['sol'] = {}
                resultado_agrupado[usuario_id][fecha]['sol'].update({'tiempo': registro['tiempo']})

            # Cálculo de las horas dormidas
            registros_dormir = Dormir.objects.values('fecha', 'hora', 'usuario_id')
            registros_despertar = Despertar.objects.values('fecha', 'hora', 'usuario_id', 'estado')

            # Agrupar registros de dormir y despertar por usuario y fecha
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
                    # Calcular el tiempo dormido
                    hora_dormir = datetime.combine(dormir['fecha'], dormir['hora'])
                    hora_despertar = datetime.combine(despertar['fecha'], despertar['hora'])

                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)  # Ajustar si la hora de despertar es al día siguiente

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

            # Obtener información adicional del usuario
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario__id__in=resultado_agrupado.keys()).values('usuario_id', 'nombres_apellidos', 'telefono')

            # Crear un diccionario para acceder a los datos del usuario por ID
            datos_personales_dict = {datos['usuario_id']: {'nombres_apellidos': datos['nombres_apellidos'], 'telefono': datos['telefono']} for datos in datos_personales}

            # Convertir el resultado agrupado en una lista
            resultado_final = []
            for usuario_id, fechas in resultado_agrupado.items():
                for fecha, datos in fechas.items():
                    # Normalizar las horas y minutos
                    if 'descanso' in datos:
                        total_horas = datos['descanso']['total_horas']
                        total_minutos = datos['descanso']['total_minutos']
                        # Ajustar minutos para que no superen las 60 unidades
                        total_horas += total_minutos // 60
                        total_minutos = total_minutos % 60
                        datos['descanso']['total_horas'] = total_horas
                        datos['descanso']['total_minutos'] = total_minutos

                    # Agregar información del usuario
                    datos_usuario = datos_personales_dict.get(usuario_id, {})
                    datos['usuario'] = datos_usuario

                    resultado_final.append({
                        'fecha': fecha,
                        'usuario': datos_usuario,
                        **datos
                    })

            return Response(resultado_final, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)