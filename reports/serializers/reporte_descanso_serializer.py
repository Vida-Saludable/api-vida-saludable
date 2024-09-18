from rest_framework import serializers


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