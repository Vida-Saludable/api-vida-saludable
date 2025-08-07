from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models.proyecto_model import Proyecto
from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.proyecto_serializer import ProyectoSerializer
from users.serializers.usuario_serializer import UsuarioSerializer
class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]
    # x

    def get_queryset(self):
        all_projects = self.request.query_params.get('all', 'false').lower() == 'true'
        
        if all_projects:
            return Proyecto.objects.all()
        
        usuario = self.request.user
        proyectos_ids = UsuarioProyecto.objects.filter(usuario=usuario).values_list('proyecto_id', flat=True)
        return Proyecto.objects.filter(id__in=proyectos_ids)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "success": True,
            "message": "Proyecto registrado correctamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "success": True,
            "message": "Proyecto actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        estado = serializer.validated_data.get('estado')
        if estado is not None:
            instance.estado = estado
        instance.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Proyecto eliminado correctamente"
        }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()