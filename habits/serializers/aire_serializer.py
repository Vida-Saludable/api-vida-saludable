from api import serializers
from models.aire_model import Aire


class AireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aire
        fields ='__all__'