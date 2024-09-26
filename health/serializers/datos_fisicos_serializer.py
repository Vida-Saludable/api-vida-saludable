from rest_framework import serializers

from health.models.datos_fisicos_models import DatosFisicos

class DatosFisicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFisicos
        fields = '__all__'
