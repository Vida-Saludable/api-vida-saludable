from rest_framework import serializers

from ..models.datos_habitos_agua_model import DatosHabitosAgua


class DatosHabitosAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosAgua
        fields = '__all__'