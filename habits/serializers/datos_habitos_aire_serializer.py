from rest_framework import serializers

from ..models.datos_habitos_aire_model import DatosHabitosAire


class DatosHabitosAireSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosAire
        fields = '__all__'