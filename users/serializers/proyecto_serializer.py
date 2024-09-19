
from api import serializers
from models.proyecto_model import Proyecto



class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'