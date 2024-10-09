from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.esperanza_model import Esperanza

class ClasificacionEsperanzaUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        tipo_practica = request.query_params.get('tipo_practica', None)
        fecha = request.query_params.get('fecha', None)

        # Filtrar los registros de Esperanza según los criterios recibidos
        filtros = {}
        if tipo_practica:
            filtros['tipo_practica'] = tipo_practica
        if fecha:
            filtros['fecha'] = fecha

        # Obtener los registros de Esperanza con los filtros (si no hay filtros, trae todos)
        esperanza_qs = Esperanza.objects.filter(**filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = esperanza_qs.values_list('usuario_id', flat=True).distinct()

        # Obtener los datos personales de esos usuarios
        usuarios = DatosPersonalesUsuario.objects.filter(usuario__id__in=usuario_ids)

        # Crear respuesta
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
                    'fecha': usuario.fecha,
                    'correo': usuario.usuario.correo,
                }
                for usuario in usuarios
            ]
        }

        return Response(result, status=status.HTTP_200_OK)
