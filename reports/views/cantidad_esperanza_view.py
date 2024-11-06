from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.esperanza_model import Esperanza

class ClasificacionEsperanzaUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        tipo_practica = request.query_params.get('tipo_practica', None)
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)

        # Obtener parámetros de paginación de la URL
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)

        # Filtrar los registros de Esperanza según los criterios recibidos
        filtros = Q()
        if tipo_practica:
            filtros &= Q(tipo_practica=tipo_practica)
        if fecha_inicio and fecha_fin:
            filtros &= Q(fecha__range=[fecha_inicio, fecha_fin])

        # Obtener los registros de Esperanza con los filtros (si no hay filtros, trae todos)
        esperanza_qs = Esperanza.objects.filter(filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = esperanza_qs.values_list('usuario_id', flat=True).distinct()

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

        # Crear respuesta con paginación
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
