from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.agua_model import Agua

class ClasificacionAguaUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        hora = request.query_params.get('hora', None)
        cantidad = request.query_params.get('cantidad', None)

        # Filtrar los registros de Agua con los criterios recibidos
        filtros = {}
        if hora:
            filtros['hora'] = hora
        if cantidad:
            filtros['cantidad'] = cantidad

        # Obtener los registros de agua con los filtros (si no hay filtros, trae todos)
        agua_qs = Agua.objects.filter(**filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = agua_qs.values_list('usuario_id', flat=True).distinct()

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
