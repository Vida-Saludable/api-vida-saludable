from rest_framework import viewsets, status
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models.dormir_model import Dormir
from ..models.despertar_model import Despertar
from ..serializers.dormir_serializer import DormirSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario

class CustomPagination(PageNumberPagination):
    page_size = 7  # Número de elementos por página
    page_size_query_param = 'page_size'  # Permite a los usuarios definir el tamaño de página en la solicitud
    max_page_size = 100  # Tamaño máximo de la página
class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
    pagination_class = CustomPagination
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
        # Obtener parámetros de búsqueda
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        # Obtener el queryset base y ordenarlo
        queryset = self.get_queryset().order_by('fecha')

        # Filtrar por usuario
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Filtrar por proyecto
        if proyecto_id:
            queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()

        resultados = []
        usuario_info = {}

        for dormir in queryset:
            usuario_id = dormir.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()

            # Agrupar por fecha
            fecha_str = dormir.fecha.strftime("%Y-%m-%d")
            if fecha_str not in usuario_info:
                usuario_info[fecha_str] = {
                    "fecha": fecha_str,
                    "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                    "telefono": datos_personales.telefono if datos_personales else None,
                    "total_horas": 0,
                    "total_minutos": 0,
                    "hora_dormir": dormir.hora.strftime("%H:%M:%S"),
                    "hora_despertar": None,  # Inicializar
                    "estado": None  # Inicializar el estado
                }

            # Obtener registros de despertar para la fecha actual
            registros_despertar = Despertar.objects.filter(usuario_id=usuario_id)

            for despertar in registros_despertar:
                if despertar.fecha >= dormir.fecha:  # Considerar solo despertares después de dormir
                    hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                    hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                    # Ajustar si la hora de despertar es al día siguiente
                    if hora_despertar < hora_dormir:
                        hora_despertar += timedelta(days=1)

                    # Calcular el tiempo dormido
                    tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                    total_horas = tiempo_dormido // 3600
                    total_minutos = (tiempo_dormido % 3600) // 60

                    usuario_info[fecha_str]["total_horas"] += int(total_horas)
                    usuario_info[fecha_str]["total_minutos"] += int(total_minutos)

                    # Guardar la última hora de despertar y el estado
                    usuario_info[fecha_str]["hora_despertar"] = despertar.hora.strftime("%H:%M:%S")
                    usuario_info[fecha_str]["estado"] = despertar.estado  # Guardar el estado

        # Convertir el diccionario a lista
        for item in usuario_info.values():
            resultados.append(item)

        # Paginación
        page = self.paginate_queryset(resultados)
        if page is not None:
            return Response({
                'success': True,
                'count': len(resultados),  # Total de elementos
                'next': self.paginator.get_next_link(),  # Enlace a la siguiente página
                'previous': self.paginator.get_previous_link(),  # Enlace a la página anterior
                'data': page  # Incluir los datos en 'data'
            }, status=status.HTTP_200_OK)

        return Response({
            'success': True,
            'message': 'Listado de registros de dormir',
            'data': resultados  # Incluir los datos en 'data'
        }, status=status.HTTP_200_OK)

