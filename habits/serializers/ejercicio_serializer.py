from api import serializers
from models.ejercicio_model import Ejercicio


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'
