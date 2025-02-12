from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from datetime import datetime, timedelta

class ClasificacionSuenioUsuariosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro de la URL
        hora_dormir = request.query_params.get('hora_dormir', None)
        hora_despertar = request.query_params.get('hora_despertar', None)

        # Filtrar los registros de Dormir y Despertar según los criterios recibidos
        filtros_dormir = {}
        filtros_despertar = {}

        if hora_dormir:
            filtros_dormir['hora'] = hora_dormir
        if hora_despertar:
            filtros_despertar['hora'] = hora_despertar

        # Obtener los registros de Dormir y Despertar filtrados
        dormir_qs = Dormir.objects.filter(**filtros_dormir).select_related('usuario')
        despertar_qs = Despertar.objects.filter(**filtros_despertar).select_related('usuario')

        # Crear un diccionario para calcular las horas de sueño
        suenio_data = {}

        for dormir in dormir_qs:
            usuario_id = dormir.usuario.id
            suenio_data[usuario_id] = {'hora_dormir': dormir.hora, 'fecha': dormir.fecha}

        for despertar in despertar_qs:
            usuario_id = despertar.usuario.id
            if usuario_id in suenio_data:
                hora_dormir = suenio_data[usuario_id]['hora_dormir']
                hora_despertar = despertar.hora

                # Calcular la diferencia de horas de sueño
                fmt = '%H:%M:%S'
                dormir_time = datetime.strptime(str(hora_dormir), fmt)
                despertar_time = datetime.strptime(str(hora_despertar), fmt)

                # Si el usuario se duerme en un día y se despierta al día siguiente
                if despertar_time < dormir_time:
                    despertar_time += timedelta(days=1)

                # Guardar la cantidad de sueño en horas
                suenio_data[usuario_id]['tiempo_suenio'] = (despertar_time - dormir_time).seconds / 3600

        # Obtener los IDs de los usuarios que tienen tanto dormir como despertar registrados
        usuario_ids = list(suenio_data.keys())

        # Obtener los datos personales de esos usuarios
        usuarios = DatosPersonalesUsuario.objects.filter(usuario__id__in=usuario_ids)

        # Crear la respuesta final con los datos de sueño y datos personales de los usuarios
        result = {
            'total_usuarios': len(usuario_ids),
            'usuarios': [
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
                    'fecha': usuario.fecha,
                    'correo': usuario.usuario.correo,
                    'tiempo_suenio': suenio_data[usuario.usuario.id]['tiempo_suenio'] if usuario.usuario.id in suenio_data else None
                }
                for usuario in usuarios
            ]
        }

        return Response(result, status=status.HTTP_200_OK)
