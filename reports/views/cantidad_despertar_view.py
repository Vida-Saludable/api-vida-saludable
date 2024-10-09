from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.despertar_model import Despertar

class ClasificacionDespertarUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        hora = request.query_params.get('hora', None)
        estado = request.query_params.get('estado', None)

        # Filtrar los registros de Despertar con los criterios recibidos
        filtros = {}
        if hora:
            filtros['hora'] = hora
        if estado:
            filtros['estado'] = estado

        # Obtener los registros de despertar con los filtros (si no hay filtros, trae todos)
        despertar_qs = Despertar.objects.filter(**filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = despertar_qs.values_list('usuario_id', flat=True).distinct()

        # Obtener los datos personales de esos usuarios
        usuarios = DatosPersonalesUsuario.objects.filter(usuario__id__in=usuario_ids)

        # Crear la respuesta
        result = {
            'total_usuarios': usuarios.count(),
            'usuarios': [
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
                for usuario in usuarios
            ]
        }

        return Response(result, status=status.HTTP_200_OK)
