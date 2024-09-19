
from rest_framework import serializers
from ..models.datos_personales_usuario_model import DatosPersonalesUsuario


class DatosPersonalesUsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = ['id', 'nombres_apellidos', 'sexo', 'edad', 'telefono', 'estado_civil']  # Campos personalizados de datos personales