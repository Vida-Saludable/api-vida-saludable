from rest_framework import serializers
from ..models.aire_model import Aire


class AireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aire
        fields ='__all__'