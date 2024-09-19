from rest_framework import serializers
from users.models.usuario_proyecto_model import UsuarioProyecto


class UsuarioProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioProyecto
        fields = '__all__'
