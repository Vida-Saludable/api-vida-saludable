from rest_framework import viewsets

from users.models.usuario_models import Usuario
from users.serializers.usuario_serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer