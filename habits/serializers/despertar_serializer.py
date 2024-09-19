from api import serializers
from models.despertar_model import Despertar


class DespertarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despertar
        fields ='__all__'