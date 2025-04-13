from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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

class ListaDatosPersonalesUsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, usuario_id=None):
        """
        Lista los datos personales de un usuario específico.
        Se puede pasar `usuario_id` como parámetro en la URL o usar el usuario autenticado.
        """
        # Si `usuario_id` no se pasa en la URL, se puede obtener del usuario autenticado
        usuario_id = usuario_id or request.user.id

        # Verificar si el `usuario_id` es válido
        if not usuario_id:
            return Response({
                "success": False,
                "message": "El ID del usuario es obligatorio."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener los datos personales del usuario
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id)

        # Verificar si se encontraron los datos personales
        if not datos_personales.exists():
            return Response({
                "success": False,
                "message": "No se encontraron datos personales para este usuario."
            }, status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos
        serializer = DatosPersonalesUsuarioSerializer(datos_personales, many=True)

        # Devolver los datos serializados como una lista de objetos
        return Response({
            "success": True,
            "data": serializer.data  # Devolver los datos como lista de objetos
        }, status=status.HTTP_200_OK)

