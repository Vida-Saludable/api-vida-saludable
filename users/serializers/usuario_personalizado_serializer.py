from api import serializers
from users.models.usuario_models import Usuario


class UsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'correo']  # Campos personalizados del usuario