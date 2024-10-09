from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_models import Usuario
from habits.models.alimentacion_model import Alimentacion


class ClasificacionAlimentacionUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        desayuno_hora = request.query_params.get('desayuno_hora', None)
        almuerzo_hora = request.query_params.get('almuerzo_hora', None)
        cena_hora = request.query_params.get('cena_hora', None)
        desayuno = request.query_params.get('desayuno', None)
        almuerzo = request.query_params.get('almuerzo', None)
        cena = request.query_params.get('cena', None)
        desayuno_saludable = request.query_params.get('desayuno_saludable', None)
        almuerzo_saludable = request.query_params.get('almuerzo_saludable', None)
        cena_saludable = request.query_params.get('cena_saludable', None)

        # Filtrar los registros de Alimentacion con los criterios recibidos
        filtros = {}
        if desayuno_hora:
            filtros['desayuno_hora'] = desayuno_hora
        if almuerzo_hora:
            filtros['almuerzo_hora'] = almuerzo_hora
        if cena_hora:
            filtros['cena_hora'] = cena_hora
        if desayuno:
            filtros['desayuno'] = desayuno
        if almuerzo:
            filtros['almuerzo'] = almuerzo
        if cena:
            filtros['cena'] = cena
        if desayuno_saludable:
            filtros['desayuno_saludable'] = desayuno_saludable
        if almuerzo_saludable:
            filtros['almuerzo_saludable'] = almuerzo_saludable
        if cena_saludable:
            filtros['cena_saludable'] = cena_saludable

        # Obtener los registros de alimentación con los filtros (si no hay filtros, trae todos)
        alimentacion_qs = Alimentacion.objects.filter(**filtros).select_related('usuario')

        # Obtener los IDs de los usuarios de esos registros
        usuario_ids = alimentacion_qs.values_list('usuario_id', flat=True).distinct()

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
