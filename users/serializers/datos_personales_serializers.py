from api import serializers
from api.models import DatosPersonalesUsuario


class DatosPersonalesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = '__all__'
