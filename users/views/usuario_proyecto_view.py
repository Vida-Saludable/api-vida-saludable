from rest_framework import viewsets

from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.usuario_proyecto_serializer import UsuarioProyectoSerializer
class UsuarioProyectoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProyecto.objects.all()
    serializer_class = UsuarioProyectoSerializer
    # permission_classes = [IsAuthenticated]
