
from api import serializers
from api.models import DatosPersonalesUsuario


class DatosPersonalesUsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = ['id', 'nombres_apellidos', 'sexo', 'edad', 'telefono', 'estado_civil']  # Campos personalizados de datos personales