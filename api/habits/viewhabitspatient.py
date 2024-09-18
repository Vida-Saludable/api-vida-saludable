# views.py
from collections import defaultdict
from datetime import datetime, timedelta
from multiprocessing import Value
from django.forms import CharField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F, Case, When
from django.db.models.functions import ExtractWeek, ExtractIsoWeekDay, Coalesce

from api.serializers import AguaSerializer, AireSerializer, AlimentacionSerializer, EjercicioSerializer, EsperanzaSerializer, SolSerializer
from ..models import Agua, Aire, Alimentacion, DatosPersonalesUsuario, Despertar, Dormir, Ejercicio, Esperanza, Sol
from ..serializershabits import ReporteAguaSerializer, ReporteAireSerializer, ReporteEjercicioPorcetajeSerializer, ReporteEjercicioSerializer, ReporteEjercicioTipoSerializer, ReporteEsperanzaPorcentajeSerializer, ReporteHorasDormidasSerializer, ReportePorcentajeDescansoSerializer, ReporteSolSerializer

class ReporteAguaView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Agua.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la cantidad de agua tomada por día durante la semana
        queryset = (
            Agua.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(cantidad_agua=Sum('cantidad'))
            .order_by('fecha_dia')
        )

        serializer = ReporteAguaSerializer(queryset, many=True)
        return Response(serializer.data)


class ReporteAireView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Aire.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la tiempo total en minutos por día durante la semana
        queryset = (
            Aire.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(tiempo_total=Sum('tiempo'))
            .order_by('fecha_dia')
        )

        serializer = ReporteAireSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ReporteEjercicioView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Ejercicio.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la tiempo total en minutos por día durante la semana
        queryset = (
            Ejercicio.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(tiempo_total=Sum('tiempo'))
            .order_by('fecha_dia')
        )

        serializer = ReporteEjercicioSerializer(queryset, many=True)
        return Response(serializer.data)


class ReporteEjercicioPorcentajeView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario tiene ejercicios registrados
        if not Ejercicio.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no tiene registros de ejercicio."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los ejercicios del usuario
        ejercicios = Ejercicio.objects.filter(usuario_id=usuario_id)
        total_ejercicios = ejercicios.count()

        # Contar la cantidad de ejercicios de cada tipo
        tipo_ejercicios = (
            ejercicios
            .values('tipo')
            .annotate(conteo=Count('tipo'))
        )

        # Inicializar contadores para los tipos de ejercicio
        conteo_ejercicios = {
            'caminata lenta': 0,
            'caminata rapida': 0,
            'trote': 0,
            'ejercicio guiado': 0,
        }

        # Llenar los contadores con los valores reales
        for tipo in tipo_ejercicios:
            conteo_ejercicios[tipo['tipo']] = tipo['conteo']

        # Calcular los porcentajes de cada tipo de ejercicio
        def calcular_porcentaje(cantidad, total):
            return round((cantidad / total) * 100, 2) if total > 0 else 0

        # Crear el diccionario de resultados
        reporte = {
            'total_ejercicios': total_ejercicios,
            'caminata_lenta': calcular_porcentaje(conteo_ejercicios['caminata lenta'], total_ejercicios),
            'caminata_rapida': calcular_porcentaje(conteo_ejercicios['caminata rapida'], total_ejercicios),
            'trote': calcular_porcentaje(conteo_ejercicios['trote'], total_ejercicios),
            'ejercicio_guiado': calcular_porcentaje(conteo_ejercicios['ejercicio guiado'], total_ejercicios),
        }

        # Serializar los datos y devolver la respuesta
        serializer = ReporteEjercicioPorcetajeSerializer(reporte)
        return Response(serializer.data)
    
class ReporteEjercicioTipoView(APIView):
    def get(self, request, usuario_id, tipo_ejercicio):
        # Verificar si el usuario tiene ejercicios registrados de ese tipo
        if not Ejercicio.objects.filter(usuario_id=usuario_id, tipo=tipo_ejercicio).exists():
            return Response({"detail": "No se encontraron ejercicios para este usuario con el tipo especificado."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el tiempo total en minutos por día durante la semana, filtrando por tipo
        queryset = (
            Ejercicio.objects
            .filter(usuario_id=usuario_id, tipo=tipo_ejercicio)  # Filtrar por usuario y tipo de ejercicio
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana como número (1-7)
            )
            .values('fecha_dia', 'dia_semana')  # Agrupar por fecha y día de la semana
            .annotate(tiempo_total=Sum('tiempo'))  # Sumar el tiempo total
            .order_by('fecha_dia')  # Ordenar por fecha
        )

        serializer = ReporteEjercicioTipoSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ReporteEsperanzaPorcentajeView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario tiene registros de esperanza
        if not Esperanza.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no tiene registros de esperanza."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todos los registros de esperanza del usuario
        esperanzas = Esperanza.objects.filter(usuario_id=usuario_id)
        total_tipo = esperanzas.count()

        # Contar la cantidad de registros por tipo de práctica
        tipo_esperanzas = (
            esperanzas
            .values('tipo_practica')
            .annotate(conteo=Count('tipo_practica'))
        )

        # Inicializar contadores para los tipos de práctica
        conteo_esperanzas = {
            'oracion': 0,
            'lectura biblica': 0,
        }

        # Llenar los contadores con los valores reales
        for tipo in tipo_esperanzas:
            conteo_esperanzas[tipo['tipo_practica']] = tipo['conteo']

        # Calcular los porcentajes de cada tipo de práctica
        def calcular_porcentaje(cantidad, total):
            return round((cantidad / total) * 100, 2) if total > 0 else 0

        # Crear el diccionario de resultados
        reporte = {
            'total_tipo': total_tipo,
            'tipo_oracion': calcular_porcentaje(conteo_esperanzas['oracion'], total_tipo),
            'tipo_lectura': calcular_porcentaje(conteo_esperanzas['lectura biblica'], total_tipo),
        }

        # Serializar los datos y devolver la respuesta
        serializer = ReporteEsperanzaPorcentajeSerializer(reporte)
        return Response(serializer.data)

class ReporteSolView(APIView):
    def get(self, request, usuario_id):
        # Verificar si el usuario existe
        if not Sol.objects.filter(usuario_id=usuario_id).exists():
            return Response({"detail": "El usuario no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la tiempo total en minutos por día durante la semana
        queryset = (
            Sol.objects
            .filter(usuario_id=usuario_id, fecha__week=ExtractWeek(F('fecha')))
            .annotate(
                fecha_dia=F('fecha'),  # Obtener la fecha completa
                dia_semana=ExtractIsoWeekDay(F('fecha'))  # Día de la semana
            )
            .values('fecha_dia', 'dia_semana')
            .annotate(tiempo_total=Sum('tiempo'))
            .order_by('fecha_dia')
        )

        serializer = ReporteSolSerializer(queryset, many=True)
        return Response(serializer.data)
    

class ReporteHorasDormidasView(APIView):
    def get(self, request, usuario_id):
        try:
            # Obtener registros de Dormir y Despertar para el usuario
            registros_dormir = Dormir.objects.filter(usuario_id=usuario_id)
            registros_despertar = Despertar.objects.filter(usuario_id=usuario_id)

            # Anotar el día de la semana para los registros de dormir
            registros_dormir = registros_dormir.annotate(
                dia_semana=ExtractIsoWeekDay('fecha')
            )

            resultados = []

            for dormir in registros_dormir:
                despertar = registros_despertar.filter(
                    fecha=dormir.fecha,
                    hora__gte=dormir.hora
                ).order_by('hora').first()

                if not despertar:
                    despertar = registros_despertar.filter(
                        fecha=dormir.fecha + timedelta(days=1),
                        hora__lt=dormir.hora
                    ).order_by('hora').first()

                if despertar:
                    # Calcular el tiempo dormido
                    hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                    hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)  # Ajustar si la hora de despertar es al día siguiente

                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    total_horas = tiempo_dormido // 3600
                    total_minutos = (tiempo_dormido % 3600) // 60

                    fecha_dia = dormir.fecha.strftime('%Y-%m-%d')
                    dia_semana = dormir.dia_semana  # Extraído por ExtractIsoWeekDay

                    resultados.append({
                        'fecha_dia': fecha_dia,
                        'dia_semana': dia_semana,
                        'total_horas': int(total_horas),
                        'total_minutos': int(total_minutos)
                    })

            serializer = ReporteHorasDormidasSerializer(resultados, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({"detail": "Error al procesar los datos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ReportePorcentajeDescansoView(APIView):
    def get(self, request, usuario_id):
        try:
            registros = Despertar.objects.filter(usuario_id=usuario_id)
            
            if not registros.exists():
                return Response({"detail": "No hay registros de despertar para este usuario."}, status=status.HTTP_404_NOT_FOUND)

            total_registros = registros.count()
            
            conteo_estados = registros.values('estado').annotate(total=Count('estado'))
            estado_counts = {estado['estado']: estado['total'] for estado in conteo_estados}

            estado_0_count = estado_counts.get(0, 0)
            estado_1_count = estado_counts.get(1, 0)

            descanso_mal = (estado_0_count / total_registros) * 100
            descanso_bien = (estado_1_count / total_registros) * 100

            resultado = {
                "total_registros": total_registros,
                "descanso_mal": round(descanso_mal, 2),
                "descanso_bien": round(descanso_bien, 2)
            }

            serializer = ReportePorcentajeDescansoSerializer(resultado)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({"detail": "Error al procesar los datos."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Reporte general de registros de habitos de cada persona por dia
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