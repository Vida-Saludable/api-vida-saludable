from rest_framework import serializers

from ..models.datos_habitos_sol_model import DatosHabitosSol


class DatosHabitosSolSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitosSol
        fields = '__all__'