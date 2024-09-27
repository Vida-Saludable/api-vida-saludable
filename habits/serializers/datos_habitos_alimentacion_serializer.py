from rest_framework import serializers

from ..models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion


class DatosHabitosAlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosAlimentacion
        fields = '__all__'