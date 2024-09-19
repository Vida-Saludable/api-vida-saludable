from rest_framework import serializers
from ..models.dormir_model import Dormir


class DormirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormir
        fields = '__all__'