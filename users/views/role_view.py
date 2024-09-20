from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models.role_model import Role
from users.serializers.role_serializer import RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAuthenticated]









