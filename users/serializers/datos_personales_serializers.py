from rest_framework import serializers
from ..models.datos_personales_usuario_model import DatosPersonalesUsuario


class DatosPersonalesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = '__all__'
