from rest_framework import serializers
from ..models.esperanza_model import Esperanza


class EsperanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esperanza
        fields = '__all__'