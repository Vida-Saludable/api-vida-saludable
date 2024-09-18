from rest_framework import serializers

from health.models.datos_corporales_models import DatosCorporales

class DatosCorporalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosCorporales
        fields = '__all__'
