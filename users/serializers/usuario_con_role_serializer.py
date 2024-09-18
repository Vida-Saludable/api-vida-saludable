
from api import serializers
from api.models import DatosPersonalesUsuario
from users.models.usuario_models import Usuario
from users.serializers.datos_personales_usuario_personalizado_serializer import DatosPersonalesUsuarioPersonalizadoSerializer


class UsuarioWithRoleSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    datos_personales = serializers.SerializerMethodField()  # Cambiado a SerializerMethodField

    class Meta:
        model = Usuario
        fields = ['id', 'correo', 'role_name', 'datos_personales']  # Ajustado para reflejar los campos correctos

    def get_role_name(self, obj):
        return obj.role.name if obj.role else None

    def get_datos_personales(self, obj):
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario=obj).first()
        if datos_personales:
            return DatosPersonalesUsuarioPersonalizadoSerializer(datos_personales).data
        return None