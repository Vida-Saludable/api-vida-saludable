# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models.proyecto_model import Proyecto
from users.models.usuario_models import Usuario
from users.models.usuario_proyecto_model import UsuarioProyecto
from users.serializers.usuario_con_role_serializer import UsuarioWithRoleSerializer


class UsersProjectView(APIView):
    def get(self, request, proyecto_id, *args, **kwargs):
        # Verificar si el proyecto existe
        if not Proyecto.objects.filter(id=proyecto_id).exists():
            return Response({"detail": "El proyecto no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener los usuarios asociados al proyecto
        usuario_proyectos = UsuarioProyecto.objects.filter(proyecto_id=proyecto_id)
        usuarios_ids = usuario_proyectos.values_list('usuario_id', flat=True)

        if not usuarios_ids:
            return Response({"detail": "No se encontraron usuarios para este proyecto."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener los usuarios asociados al proyecto
        usuarios = Usuario.objects.filter(id__in=usuarios_ids)

        # Paginación
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        
        paginator = Paginator(usuarios, page_size)
        try:
            usuarios_paginados = paginator.page(page)
        except PageNotAnInteger:
            usuarios_paginados = paginator.page(1)
        except EmptyPage:
            usuarios_paginados = paginator.page(paginator.num_pages)

        serializer = UsuarioWithRoleSerializer(usuarios_paginados, many=True)
        
        # Construir la respuesta con la paginación
        response_data = {
            "data": serializer.data,
            "totalItems": paginator.count,
            "page": int(page),
            "pageSize": int(page_size),
            "totalPages": paginator.num_pages
        }

        return Response(response_data, status=status.HTTP_200_OK)
