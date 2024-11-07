from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from decimal import Decimal
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario 
from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales

from .analizadorsalud import AnalizadorSalud
from statistics import mean

class IndicadoresSaludPorUsuarioView(APIView):

    def get(self, request, usuario_id, *args, **kwargs):
        # Obtener los datos personales del usuario específico
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).select_related('usuario')

        # Verificar si se encontraron datos personales para el usuario
        if not datos_personales.exists():
            return Response({"detail": "No se encontraron datos personales para este usuario."}, status=status.HTTP_404_NOT_FOUND)

        # Crear un diccionario para acceder fácilmente al sexo del usuario
        sexo_usuario = {dato.usuario_id: dato.sexo for dato in datos_personales}

        # Obtener los datos de los cuatro modelos relacionados con el usuario
        datos_fisicos = DatosFisicos.objects.filter(usuario_id=usuario_id, tipo='inicial')
        datos_muestras = DatosMuestras.objects.filter(usuario_id=usuario_id, tipo='inicial')
        signos_vitales = SignosVitales.objects.filter(usuario_id=usuario_id, tipo='inicial')
      

        # Verificar si se encontraron datos en al menos uno de los modelos
        if not (datos_fisicos.exists() or datos_muestras.exists() or signos_vitales.exists()):
            return Response({"detail": "No se encontraron datos de salud para este usuario."}, status=status.HTTP_404_NOT_FOUND)

        # Inicializar acumuladores para los indicadores
        indicadores = {
            'peso': [],
            'altura': [],
            'imc': [],
            'radio_abdominal': {'M': [], 'F': []},
            'porcentaje_musculo': {'M': [], 'F': []},
            'grasa_corporal': {'M': [], 'F': []},
            'grasa_visceral': [],
            'colesterol_total': [],
            'colesterol_hdl': {'M': [], 'F': []},
            'colesterol_ldl': [],
            'trigliceridos': [],
            'glucosa': [],
            'presion_sistolica': [],
            'presion_diastolica': [],
            'frecuencia_cardiaca': [],
            'frecuencia_respiratoria': [],
            'saturacion_oxigeno': [],
            'glicemia_basal': [],
            'temperatura': [],
        }

        # Procesar datos de DatosFisicos
        for dato in datos_fisicos:
            sexo = sexo_usuario.get(dato.usuario_id, 'M')  # Por defecto 'M' si no se encuentra el sexo
            indicadores['peso'].append(dato.peso)
            indicadores['altura'].append(dato.altura)
            indicadores['imc'].append(dato.imc)
            indicadores['radio_abdominal'][sexo].append(dato.radio_abdominal)
            indicadores['porcentaje_musculo'][sexo].append(dato.porcentaje_musculo)
            indicadores['grasa_corporal'][sexo].append(dato.grasa_corporal)
            indicadores['grasa_visceral'].append(dato.grasa_visceral)

        # Procesar datos de DatosMuestras
        for dato in datos_muestras:
            sexo = sexo_usuario.get(dato.usuario_id, 'M')
            indicadores['colesterol_total'].append(dato.colesterol_total)
            indicadores['colesterol_hdl'][sexo].append(dato.colesterol_hdl)
            indicadores['colesterol_ldl'].append(dato.colesterol_ldl)
            indicadores['trigliceridos'].append(dato.trigliceridos)
            indicadores['glucosa'].append(dato.glucosa)
            indicadores['glicemia_basal'].append(dato.glicemia_basal)

        # Procesar datos de SignosVitales
        for dato in signos_vitales:
            indicadores['presion_sistolica'].append(dato.presion_sistolica)
            indicadores['presion_diastolica'].append(dato.presion_diastolica)
            indicadores['frecuencia_cardiaca'].append(dato.frecuencia_cardiaca)
            indicadores['frecuencia_respiratoria'].append(dato.frecuencia_respiratoria)
            indicadores['saturacion_oxigeno'].append(dato.saturacion_oxigeno)
            indicadores['temperatura'].append(dato.temperatura)



        # Calcular el promedio de cada indicador
        promedios = {}
        for clave, valores in indicadores.items():
            if isinstance(valores, dict):
                promedios[clave] = {}
                for subclave, subvalores in valores.items():
                    if subvalores:
                        promedios[clave][subclave] = mean(subvalores)
                    else:
                        promedios[clave][subclave] = None
            else:
                if valores:
                    promedios[clave] = mean(valores)
                else:
                    promedios[clave] = None

        # Construir los resultados eliminando "M" o "F" si no son necesarios
        resultados = {}
        for clave, promedio in promedios.items():
            if clave in ['radio_abdominal', 'grasa_corporal', 'colesterol_hdl', 'porcentaje_musculo']:
                if promedios[clave]['M'] is not None:
                    resultados[clave] = {
                        'promedio': promedios[clave]['M'],
                        'data': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedios[clave]['M'], 'M')
                    }
                elif promedios[clave]['F'] is not None:
                    resultados[clave] = {
                        'promedio': promedios[clave]['F'],
                        'data': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedios[clave]['F'], 'F')
                    }
            else:
                resultados[clave] = {
                    'promedio': promedio,
                    'data': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio) if promedio is not None else None
                }

        return Response(resultados, status=status.HTTP_200_OK)
