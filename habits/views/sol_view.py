from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.sol_model import Sol
from ..serializers.sol_serializer import SolSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class SolViewSet(viewsets.ModelViewSet):
    queryset = Sol.objects.all()
    serializer_class = SolSerializer
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
        data = []
        usuario_info = {}

        for sol in queryset:
            usuario_id = sol.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Agrupar por fecha
            fecha_str = sol.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "tiempo": 0,  # Iniciar con 0
                }

            # Sumar el tiempo de sol
            usuario_info[fecha_str]["tiempo"] += sol.tiempo  # Sumar el tiempo total

        # Convertir el diccionario a lista
        for item in usuario_info.values():
            data.append(item)

        return Response({
            'success': True,
            'message': 'Listado de registros de sol',
            'data': data
        })
