from rest_framework import serializers


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