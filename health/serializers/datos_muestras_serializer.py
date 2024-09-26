from rest_framework import serializers

from health.models.datos_muestras_models import DatosMuestras

class DatosMuestrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosMuestras
        fields = '__all__'
