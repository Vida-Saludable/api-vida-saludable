from rest_framework import serializers

from ..models.datos_habitos_esperanza_model import DatosHabitosEsperanza


class DatosHabitosEsperanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosEsperanza
        fields = '__all__'