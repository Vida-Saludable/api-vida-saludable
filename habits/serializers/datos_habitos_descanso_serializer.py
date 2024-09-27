from rest_framework import serializers

from ..models.datos_habitos_descanso_model import DatosHabitosDescanso


class DatosHabitosDescansoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosDescanso
        fields = '__all__'