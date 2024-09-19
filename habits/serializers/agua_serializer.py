from rest_framework import serializers
from ..models.agua_model import Agua


class AguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agua
        fields = '__all__'