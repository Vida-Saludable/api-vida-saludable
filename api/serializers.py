from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Role, Usuario, DatosPersonalesUsuario, Alimentacion, Agua, Esperanza, Sol, Aire, Dormir,
    Despertar, Ejercicio, Proyecto, UsuarioProyecto, DatosCorporales, DatosHabitos
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


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


# serializers.py



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar más datos al token aquí si lo deseas

        return token


class DatosPersonalesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = '__all__'

class UsuarioProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioProyecto
        fields = '__all__'


class AlimentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimentacion
        fields = '__all__'


class AguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agua
        fields = '__all__'


class EsperanzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Esperanza
        fields = '__all__'


class SolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sol
        fields = '__all__'


class AireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aire
        fields ='__all__'


class DormirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormir
        fields = '__all__'


class DespertarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despertar
        fields ='__all__'


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'




class DatosCorporalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosCorporales
        fields = '__all__'



class DatosHabitosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosHabitos
        fields = '__all__'




class UsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'correo']  # Campos personalizados del usuario

class DatosPersonalesUsuarioPersonalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosPersonalesUsuario
        fields = ['id', 'nombres_apellidos', 'sexo', 'edad', 'telefono', 'estado_civil']  # Campos personalizados de datos personales

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





# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     correo = serializers.EmailField(write_only=True)
#     contrasenia = serializers.CharField(write_only=True)

#     def validate(self, attrs):
#         try:
#             # Busca al usuario por el correo
#             usuario = Usuario.objects.get(correo=attrs['correo'])
#         except Usuario.DoesNotExist:
#             raise serializers.ValidationError('Usuario no encontrado.')

#         # Verifica la contraseña
#         if not usuario.check_password(attrs['contrasenia']):
#             raise serializers.ValidationError('Contraseña incorrecta.')

#         # Si la autenticación es correcta, genera el token
#         data = super().validate({
#             'username': usuario.correo,  # Envío correo como 'username' por compatibilidad con JWT
#             'password': attrs['contrasenia'],
#         })

#         # Añade campos adicionales si es necesario
#         data['usuario_id'] = usuario.id
#         data['role'] = usuario.role.name if usuario.role else None  # Devuelve el role del usuario
#         return data
