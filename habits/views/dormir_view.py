from rest_framework import viewsets, status
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from ..models.dormir_model import Dormir
from ..models.despertar_model import Despertar
from ..serializers.dormir_serializer import DormirSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto

class CustomPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 100

class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Obtener proyectos del usuario para la respuesta
        usuario_id = request.data.get('usuario')
        proyectos_usuario = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)
        
        response_data = serializer.data
        response_data['proyectos_usuario'] = list(proyectos_usuario)
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Se registró exitosamente',
            'data': response_data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)
        usuario_autenticado = request.user

        # Obtener proyectos del usuario autenticado
        proyectos_usuario = UsuarioProyecto.objects.filter(usuario=usuario_autenticado).values_list('proyecto_id', flat=True)
        
        queryset = self.get_queryset().order_by('fecha')
        
        # Filtrar solo registros de usuarios que estén en los proyectos del usuario autenticado
        queryset = queryset.filter(usuario__usuarioproyecto__proyecto_id__in=proyectos_usuario).distinct()

        # Filtrar por usuario si se proporciona
        if usuario:
            queryset = queryset.filter(usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario)

        # Filtrar por proyecto específico si se indica
        if proyecto_id and proyecto_id.lower() not in ['all', 'todos']:
            queryset = queryset.filter(usuario__usuarioproyecto__proyecto__id=proyecto_id).distinct()

        paginated_queryset = self.paginate_queryset(queryset)

        usuario_info = []
        for dormir in paginated_queryset:
            usuario_id = dormir.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            proyectos = UsuarioProyecto.objects.filter(usuario_id=usuario_id).values_list('proyecto__nombre', flat=True)

            item = {
                "fecha": dormir.fecha.strftime("%Y-%m-%d"),
                "usuario": datos_personales.nombres_apellidos if datos_personales else None,
                "telefono": datos_personales.telefono if datos_personales else None,
                "total_horas": 0,
                "total_minutos": 0,
                "hora_dormir": dormir.hora.strftime("%H:%M:%S"),
                "hora_despertar": None,
                "estado": None,
                "proyectos_usuario": list(proyectos) if proyectos else []
            }

            registros_despertar = Despertar.objects.filter(
                usuario_id=usuario_id,
                fecha__gte=dormir.fecha
            ).order_by('fecha', 'hora')

            for despertar in registros_despertar:
                hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                if hora_despertar < hora_dormir:
                    hora_despertar += timedelta(days=1)

                tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                horas = int(tiempo_dormido // 3600)
                minutos = int((tiempo_dormido % 3600) // 60)

                item["total_horas"] += horas
                item["total_minutos"] += minutos

                if item["total_minutos"] >= 60:
                    item["total_horas"] += item["total_minutos"] // 60
                    item["total_minutos"] = item["total_minutos"] % 60

                item["hora_despertar"] = despertar.hora.strftime("%H:%M:%S")
                item["estado"] = despertar.estado

                break

            usuario_info.append(item)

        page = self.paginator
        return Response({
            "success": True,
            "count": page.page.paginator.count,
            "next": page.get_next_link(),
            "previous": page.get_previous_link(),
            "data": usuario_info
        }, status=status.HTTP_200_OK)