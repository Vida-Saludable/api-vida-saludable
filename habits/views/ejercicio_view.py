from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.ejercicio_model import Ejercicio
from ..serializers.ejercicio_serializer import EjercicioSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Se registró exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Modificar los datos para agregar nombres_apellidos y telefono del usuario
        for item in data:
            usuario_id = item['usuario']  # Obtener el id del usuario
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            if datos_personales:
                item['usuario'] = datos_personales.nombres_apellidos  # Reemplazar el ID con nombres_apellidos
                item['telefono'] = datos_personales.telefono  # Agregar el telefono
            else:
                item['usuario'] = None
                item['telefono'] = None

        return Response({
            'success': True,
            'message': 'Listado de registros de ejercicio',
            'data': data
        })
