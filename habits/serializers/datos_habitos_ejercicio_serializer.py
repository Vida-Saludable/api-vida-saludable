from rest_framework import serializers

from ..models.datos_habitos_ejercicio_model import DatosHabitosEjercicio


class DatosHabitosEjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosEjercicio
        fields = '__all__'