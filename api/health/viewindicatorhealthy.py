from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from decimal import Decimal
from ..models import DatosCorporales, DatosPersonalesUsuario
from ..serializers import DatosCorporalesSerializer
from .analizadorsalud import AnalizadorSalud
from statistics import mean

class IndicadoresSaludPorUsuarioView(APIView):

    def get(self, request, usuario_id, *args, **kwargs):
        # Obtener los datos corporales y datos personales del usuario específico
        datos_corporales = DatosCorporales.objects.filter(usuario_id=usuario_id, tipo='inicial').select_related('usuario')
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).select_related('usuario')

        # Verificar si se encontraron datos para el usuario
        if not datos_corporales.exists() or not datos_personales.exists():
            return Response({"detail": "No se encontraron datos corporales o personales para este usuario."}, status=status.HTTP_404_NOT_FOUND)

        # Crear un diccionario para acceder fácilmente al sexo del usuario
        sexo_usuario = {dato.usuario_id: dato.sexo for dato in datos_personales}

        # Inicializar acumuladores para los promedios
        indicadores = {
            'peso': [],
            'altura': [],
            'imc': [],
            'presion_sistolica': [],
            'presion_diastolica': [],
            'radio_abdominal': {'M': [], 'F': []},
            'grasa_corporal': {'M': [], 'F': []},
            'grasa_visceral': [],
            'frecuencia_cardiaca': [],
            'frecuencia_respiratoria': [],
            'colesterol_total': [],
            'colesterol_hdl': {'M': [], 'F': []},
            'colesterol_ldl': [],
            'trigliceridos': [],
            'glucosa': [],
            'temperatura': [],
            'saturacion_oxigeno': [],
            'porcentaje_musculo': {'M': [], 'F': []},
            'glicemia_basal': [],
            'frecuencia_cardiaca_en_reposo': [],
            'frecuencia_cardiaca_despues_de_45_segundos': [],
            'frecuencia_cardiaca_1_minuto_despues': [],
            'resultado_test_rufier': [],
        }

        for dato in datos_corporales:
            usuario_id = dato.usuario_id
            sexo = sexo_usuario.get(usuario_id, 'M')  # Por defecto 'M' si no se encuentra el sexo

            indicadores['peso'].append(dato.peso)
            indicadores['altura'].append(dato.altura)
            indicadores['imc'].append(dato.imc)
            indicadores['presion_sistolica'].append(dato.presion_sistolica)
            indicadores['presion_diastolica'].append(dato.presion_diastolica)
            indicadores['radio_abdominal'][sexo].append(dato.radio_abdominal)
            indicadores['grasa_corporal'][sexo].append(dato.grasa_corporal)
            indicadores['grasa_visceral'].append(dato.grasa_visceral)
            indicadores['frecuencia_cardiaca'].append(dato.frecuencia_cardiaca)
            indicadores['frecuencia_respiratoria'].append(dato.frecuencia_respiratoria)
            indicadores['colesterol_total'].append(dato.colesterol_total)
            indicadores['colesterol_hdl'][sexo].append(dato.colesterol_hdl)
            indicadores['colesterol_ldl'].append(dato.colesterol_ldl)
            indicadores['trigliceridos'].append(dato.trigliceridos)
            indicadores['glucosa'].append(dato.glucosa)
            indicadores['temperatura'].append(dato.temperatura)
            indicadores['saturacion_oxigeno'].append(dato.saturacion_oxigeno)
            indicadores['porcentaje_musculo'][sexo].append(dato.porcentaje_musculo)
            indicadores['glicemia_basal'].append(dato.glicemia_basal)
            indicadores['frecuencia_cardiaca_en_reposo'].append(dato.frecuencia_cardiaca_en_reposo)
            indicadores['frecuencia_cardiaca_despues_de_45_segundos'].append(dato.frecuencia_cardiaca_despues_de_45_segundos)
            indicadores['frecuencia_cardiaca_1_minuto_despues'].append(dato.frecuencia_cardiaca_1_minuto_despues)
            indicadores['resultado_test_rufier'].append(dato.resultado_test_rufier)

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
                        'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedios[clave]['M'], 'M')
                    }
                elif promedios[clave]['F'] is not None:
                    resultados[clave] = {
                        'promedio': promedios[clave]['F'],
                        'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedios[clave]['F'], 'F')
                    }
            else:
                resultados[clave] = {
                    'promedio': promedio,
                    'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio) if promedio is not None else None
                }

        return Response(resultados, status=status.HTTP_200_OK)
