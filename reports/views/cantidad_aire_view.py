from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.aire_model import Aire

class ClasificacionAireUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        tiempo = request.query_params.get('tiempo', None)
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)

        # Obtener parámetros de paginación de la URL
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)

        # Filtrar los registros de Aire con los criterios recibidos
        filtros = Q()
        if tiempo:
            filtros &= Q(tiempo=tiempo)
        if fecha_inicio and fecha_fin:
            filtros &= Q(fecha__range=[fecha_inicio, fecha_fin])

        # Obtener los registros de aire con los filtros (si no hay filtros, trae todos)
        aire_qs = Aire.objects.filter(filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = aire_qs.values_list('usuario_id', flat=True).distinct()

        # Obtener los datos personales de esos usuarios
        usuarios = DatosPersonalesUsuario.objects.filter(usuario__id__in=usuario_ids)

        # Configurar la paginación
        paginator = Paginator(usuarios, page_size)
        try:
            usuarios_paginados = paginator.page(page)
        except PageNotAnInteger:
            usuarios_paginados = paginator.page(1)
        except EmptyPage:
            usuarios_paginados = paginator.page(paginator.num_pages)

        # Crear la respuesta con paginación
        result = {
            'data': [
                {
                    'nombres_apellidos': usuario.nombres_apellidos,
                    'sexo': usuario.sexo,
                    'edad': usuario.edad,
                    'estado_civil': usuario.estado_civil,
                    'fecha_nacimiento': usuario.fecha_nacimiento,
                    'telefono': usuario.telefono,
                    'grado_instruccion': usuario.grado_instruccion,
                    'procedencia': usuario.procedencia,
                    'religion': usuario.religion,
                    'correo': usuario.usuario.correo,
                }
                for usuario in usuarios_paginados
            ],
            'totalItems': paginator.count,
            'page': usuarios_paginados.number,
            'pageSize': page_size,
            'totalPages': paginator.num_pages,
        }

        return Response(result, status=status.HTTP_200_OK)
