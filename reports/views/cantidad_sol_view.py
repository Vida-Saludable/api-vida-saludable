from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.sol_model import Sol

class ClasificacionSolUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        tiempo = request.query_params.get('tiempo', None)
        fecha_inicio = request.query_params.get('fecha_inicio', None)
        fecha_fin = request.query_params.get('fecha_fin', None)
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        filtros = {}
        if tiempo:
            filtros['tiempo'] = tiempo
        if fecha_inicio and fecha_fin:
            filtros['fecha__range'] = [fecha_inicio, fecha_fin]
        sol_qs = Sol.objects.filter(**filtros).select_related('usuario')
        usuario_ids = sol_qs.values_list('usuario_id', flat=True).distinct()
        usuarios = DatosPersonalesUsuario.objects.filter(usuario__id__in=usuario_ids)
        paginator = Paginator(usuarios, page_size)
        try:
            usuarios_paginados = paginator.page(page)
        except PageNotAnInteger:
            usuarios_paginados = paginator.page(1)
        except EmptyPage:
            usuarios_paginados = paginator.page(paginator.num_pages)
        result = {
            'data': [
                {
                    'nombres_apellidos': usuario.nombres_apellidos,
                    'sexo': usuario.sexo,
                    'edad': usuario.edad,
                    'estado_civil': usuario.estado_civil,
                    'fecha_nacimiento': usuario.fecha_nacimiento,
                    'telefono': usuario.telefono,
                    'ocupacion': usuario.ocupacion,
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
