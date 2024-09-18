# serializers.py
from rest_framework import serializers

from api.serializers import AguaSerializer, AireSerializer, AlimentacionSerializer, EjercicioSerializer, EsperanzaSerializer, SolSerializer

class ReporteAguaSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.CharField()  # Día de la semana en formato abreviado
    cantidad_agua = serializers.IntegerField()  # En mililitros

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapear el número del día de la semana a su abreviatura
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir la fecha a string y el día de la semana a su abreviatura
        representation['dia_semana'] = dias_semana.get(int(representation['dia_semana']), 'Unknown')
        representation['fecha_dia'] = instance['fecha_dia'].strftime('%Y-%m-%d')  # Formato completo
        return representation
    
class ReporteAireSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.CharField()  # Día de la semana en formato abreviado
    tiempo_total = serializers.IntegerField()  # En minutos

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapear el número del día de la semana a su abreviatura
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir la fecha a string y el día de la semana a su abreviatura
        representation['dia_semana'] = dias_semana.get(int(representation['dia_semana']), 'Unknown')
        representation['fecha_dia'] = instance['fecha_dia'].strftime('%Y-%m-%d')  # Formato completo
        return representation

class ReporteEjercicioSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.CharField()  # Día de la semana en formato abreviado
    tiempo_total = serializers.IntegerField()  # En minutos

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapear el número del día de la semana a su abreviatura
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir la fecha a string y el día de la semana a su abreviatura
        representation['dia_semana'] = dias_semana.get(int(representation['dia_semana']), 'Unknown')
        representation['fecha_dia'] = instance['fecha_dia'].strftime('%Y-%m-%d')  # Formato completo
        return representation
    
class ReporteEjercicioPorcetajeSerializer(serializers.Serializer):
    total_ejercicios = serializers.IntegerField()
    caminata_lenta = serializers.FloatField()
    caminata_rapida = serializers.FloatField()
    trote = serializers.FloatField()
    ejercicio_guiado = serializers.FloatField()

class ReporteEjercicioTipoSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.CharField()  # Día de la semana en formato abreviado
    tiempo_total = serializers.IntegerField()  # En minutos

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapa de abreviaturas para los días de la semana
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir el día de la semana a su abreviatura y la fecha a formato de string
        representation['dia_semana'] = dias_semana.get(int(representation['dia_semana']), 'Unknown')
        representation['fecha_dia'] = instance['fecha_dia'].strftime('%Y-%m-%d')  # Formato completo de la fecha
        return representation
    
class ReporteEsperanzaPorcentajeSerializer(serializers.Serializer):
    total_tipo = serializers.IntegerField()
    tipo_oracion = serializers.FloatField()
    tipo_lectura = serializers.FloatField()

class ReporteSolSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.CharField()  # Día de la semana en formato abreviado
    tiempo_total = serializers.IntegerField()  # En minutos

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapear el número del día de la semana a su abreviatura
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir la fecha a string y el día de la semana a su abreviatura
        representation['dia_semana'] = dias_semana.get(int(representation['dia_semana']), 'Unknown')
        representation['fecha_dia'] = instance['fecha_dia'].strftime('%Y-%m-%d')  # Formato completo
        return representation


class ReporteHorasDormidasSerializer(serializers.Serializer):
    fecha_dia = serializers.DateField()  # Día del mes
    dia_semana = serializers.IntegerField()  # Número del día de la semana
    total_horas = serializers.IntegerField()  # Total de horas dormidas
    total_minutos = serializers.IntegerField()  # Total de minutos dormidos

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Mapear el número del día de la semana a su abreviatura
        dias_semana = {
            1: 'Lun',  # Lunes
            2: 'Mar',  # Martes
            3: 'Mié',  # Miércoles
            4: 'Jue',  # Jueves
            5: 'Vie',  # Viernes
            6: 'Sáb',  # Sábado
            7: 'Dom'   # Domingo
        }
        # Convertir el número del día de la semana a su abreviatura
        dia_semana_numero = int(representation['dia_semana'])
        representation['dia_semana'] = dias_semana.get(dia_semana_numero, 'Desconocido')
        return representation

class ReportePorcentajeDescansoSerializer(serializers.Serializer):
    total_registros = serializers.IntegerField()  # Número total de registros de despertar
    descanso_mal = serializers.FloatField()  # Porcentaje de registros con estado 0
    descanso_bien = serializers.FloatField()  # Porcentaje de registros con estado 1

# Reporte general de registros de habitos de cada persona por dia
# class RegistroHabitosSerializer(serializers.Serializer):
#     alimentacion = AlimentacionSerializer(many=True)
#     aire = AireSerializer(many=True)
#     agua = AguaSerializer(many=True)
#     ejercicio = EjercicioSerializer(many=True)
#     esperanza = EsperanzaSerializer(many=True)
#     sol = SolSerializer(many=True)
#     descanso = DescansoSerializer(many=True)