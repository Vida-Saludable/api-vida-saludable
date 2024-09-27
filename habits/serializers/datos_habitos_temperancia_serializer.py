from rest_framework import serializers

from ..models.datos_habitos_temperancia_model import DatosHabitosTemperancia


class DatosHabitosTemperanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosTemperancia
        fields = '__all__'