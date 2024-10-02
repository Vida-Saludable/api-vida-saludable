from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.views import APIView

from health.models.datos_muestras_models import DatosMuestras
from health.serializers.datos_muestras_serializer import DatosMuestrasSerializer

class DatosMuestrasViewSet(viewsets.ModelViewSet):
    queryset = DatosMuestras.objects.all()
    serializer_class = DatosMuestrasSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario')  # Asegúrate de que el campo 'usuario' esté presente en los datos
        
        if not usuario_id:
            return Response({
                "success": False,
                "message": "El campo 'usuario' es obligatorio."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si hay registros previos del mismo usuario
        registros_previos = DatosMuestras.objects.filter(usuario_id=usuario_id).order_by('-fecha')

        with transaction.atomic():  # Para asegurar que las actualizaciones sean atómicas
            if not registros_previos.exists():
                # Si no hay registros previos, el tipo será 'inicial'
                request.data['tipo'] = 'inicial'
            else:
                ultimo_registro = registros_previos.first()

                if ultimo_registro.tipo == 'inicial':
                    # Si el último registro es 'inicial', este nuevo será 'final'
                    request.data['tipo'] = 'final'
                elif ultimo_registro.tipo == 'final':
                    # Si el último registro es 'final', actualizamos ese registro a 'seguimiento'
                    ultimo_registro.tipo = 'seguimiento'
                    ultimo_registro.save()

                    # El nuevo registro será 'final'
                    request.data['tipo'] = 'final'
                else:
                    # Si el último registro es 'seguimiento', el nuevo registro será 'final'
                    request.data['tipo'] = 'final'

            # Crear el nuevo registro
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Datos que se devolverán con el mensaje de éxito
                response_data = {
                    "success": True,
                    "message": "Registro de datos de muestras creado con éxito.",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                # En caso de error de validación, se devuelve el error específico
                response_data = {
                    "success": False,
                    "message": "Error al crear el registro de datos de muestras.",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
class ListaDatosMuestrasUsuarioView(APIView):
    def get(self, request, usuario_id=None):
        """
        Lista todos los registros de Datos de Muestras de un usuario específico.
        Se puede pasar `usuario_id` como parámetro en la URL o usar el usuario autenticado.
        """
        # Si `usuario_id` no se pasa en la URL, se puede obtener del usuario autenticado (si aplica)
        usuario_id = usuario_id or request.user.id

        # Verificar si el `usuario_id` es válido
        if not usuario_id:
            return Response({
                "success": False,
                "message": "El ID del usuario es obligatorio."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Obtener los registros del usuario
        registros = DatosMuestras.objects.filter(usuario_id=usuario_id).order_by('-fecha')

        # Verificar si el usuario tiene registros
        if not registros.exists():
            return Response({
                "success": False,
                "message": "No se encontraron registros para este usuario."
            }, status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos
        serializer = DatosMuestrasSerializer(registros, many=True)

        # Eliminar el campo 'id' de cada registro en los datos serializados
        data = serializer.data
        for registro in data:
            if 'id' in registro:
                del registro['id']

        # Devolver los registros serializados sin el campo 'id'
        return Response({
            "success": True,
            "data": data
        }, status=status.HTTP_200_OK)
