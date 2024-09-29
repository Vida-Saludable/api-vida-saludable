from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Min, Max, Count

from habits.models.alimentacion_model import Alimentacion
from habits.models.agua_model import Agua
from habits.models.aire_model import Aire
from habits.models.sol_model import Sol
from habits.models.esperanza_model import Esperanza
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from habits.models.ejercicio_model import Ejercicio

class GetDatesByIdView(APIView):
    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')

        # Lista de modelos para iterar
        models = [
            Alimentacion, Agua, Aire, Sol, Esperanza, Dormir, Despertar, Ejercicio
        ]

        # Lista para almacenar los resultados de cada modelo
        fechas_info = []

        for model in models:
            # Obtener fecha mínima, fecha máxima y longitud de registros para el usuario
            datos = model.objects.filter(usuario_id=usuario_id).aggregate(
                primera_fecha=Min('fecha'),
                ultima_fecha=Max('fecha'),
                cantidad=Count('id')
            )
            # Solo agregamos si hay registros (cantidad > 0)
            if datos['cantidad'] > 0:
                fechas_info.append({
                    'primera_fecha': datos['primera_fecha'],
                    'ultima_fecha': datos['ultima_fecha'],
                    'cantidad': datos['cantidad'],
                    'model': model.__name__  # Nombre del modelo para referencia
                })

        # Si no hay datos en ningún modelo, devolver un error
        if not fechas_info:
            return Response({"detail": "No se encontraron fechas para el usuario."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener las fechas mínimas y máximas
        fechas_minimas = [info['primera_fecha'] for info in fechas_info]
        fechas_maximas = [info['ultima_fecha'] for info in fechas_info]
        
        # Verificar si todas las fechas mínimas son iguales
        if len(set(fechas_minimas)) == 1:
            # Todas las fechas mínimas son iguales
            fecha_minima_final = fechas_minimas[0]
        else:
            # Devolver la fecha mínima del modelo con menos registros
            fecha_minima_final = min(fechas_info, key=lambda x: x['cantidad'])['primera_fecha']

        # Verificar si todas las fechas máximas son iguales
        if len(set(fechas_maximas)) == 1:
            # Todas las fechas máximas son iguales
            fecha_maxima_final = fechas_maximas[0]
        else:
            # Devolver la fecha máxima del modelo con menos registros
            fecha_maxima_final = min(fechas_info, key=lambda x: x['cantidad'])['ultima_fecha']

        # Devolver las fechas mínima, máxima y la longitud más baja de los datos
        return Response({
            "primera_fecha": fecha_minima_final,
            "ultima_fecha": fecha_maxima_final,
            "longitud_minima_registros": min(fechas_info, key=lambda x: x['cantidad'])['cantidad']
        }, status=status.HTTP_200_OK)
