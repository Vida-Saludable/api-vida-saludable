from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.serializers.datos_personales_serializers import DatosPersonalesUsuarioSerializer
class DatosPersonalesUsuarioViewSet(viewsets.ModelViewSet):
    queryset = DatosPersonalesUsuario.objects.all()
    serializer_class = DatosPersonalesUsuarioSerializer
    permission_classes = [IsAuthenticated]