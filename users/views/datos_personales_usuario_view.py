from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.serializers.datos_personales_serializers import DatosPersonalesUsuarioSerializer
class DatosPersonalesUsuarioViewSet(viewsets.ModelViewSet):
    queryset = DatosPersonalesUsuario.objects.all()
    serializer_class = DatosPersonalesUsuarioSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Serializa los datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Prepara la respuesta personalizada con success y message
        response_data = {
            'success': True,
            'message': 'Datos personales del usuario creados exitosamente.',
            'data': serializer.data
        }

        # Retorna la respuesta con el estatus HTTP 201 (creado)
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        # Obtén la instancia a editar
        partial = kwargs.pop('partial', False)  # Si es un PATCH (parcial)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Respuesta personalizada al editar
        response_data = {
            'success': True,
            'message': 'Datos personales del usuario actualizados exitosamente.',
            'data': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)