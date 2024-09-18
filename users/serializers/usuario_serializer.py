from api import serializers
from users.models.usuario_models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    contrasenia = serializers.CharField(write_only=True)  # Acepta contrasenia como entrada

    class Meta:
        model = Usuario
        fields = ('id', 'correo', 'contrasenia', 'role')

    def create(self, validated_data):
        # Usa set_password para asignar la contraseña correctamente
        usuario = Usuario(
            correo=validated_data['correo'],
            role=validated_data.get('role')
        )
        usuario.set_password(validated_data['contrasenia'])  # Hashea la contraseña
        usuario.save()
        return usuario