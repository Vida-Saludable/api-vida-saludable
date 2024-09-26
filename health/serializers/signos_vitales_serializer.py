from rest_framework import serializers

from health.models.signos_vitales_models import SignosVitales

class SignosVitalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignosVitales
        fields = '__all__'
