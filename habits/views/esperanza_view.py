from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.esperanza_model import Esperanza
from ..serializers.esperanza_serializer import EsperanzaSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

class EsperanzaViewSet(viewsets.ModelViewSet):
    queryset = Esperanza.objects.all()
    serializer_class = EsperanzaSerializer
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

        for esperanza in queryset:
            usuario_id = esperanza.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Agrupar por fecha
            fecha_str = esperanza.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "oracion": None,
                    "leer_biblia": None,
                }

            # Asignar el tipo de práctica
            if esperanza.tipo_practica == "oracion":
                usuario_info[fecha_str]["oracion"] = esperanza.tipo_practica
            elif esperanza.tipo_practica == "leer biblia":
                usuario_info[fecha_str]["leer_biblia"] = esperanza.tipo_practica

        # Convertir el diccionario a lista
        for item in usuario_info.values():
            data.append(item)

        return Response({
            'success': True,
            'message': 'Listado de registros de esperanza',
            'data': data
        })
