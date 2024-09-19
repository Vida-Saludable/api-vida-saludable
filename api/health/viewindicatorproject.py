from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from decimal import Decimal
from ...users.models.datos_personales_usuario_model import DatosPersonalesUsuario 
from ...users.models.proyecto_model import Proyecto 
from ...users.models.usuario_proyecto_model import UsuarioProyecto 
from ...health.models.datos_corporales_models import DatosCorporales
# from ..serializers import DatosCorporalesSerializer
from .analizadorsalud import AnalizadorSalud
from statistics import mean

class IndicadoresSaludPorProyectoView(APIView):

    def get(self, request, proyecto_id, *args, **kwargs):
        # Verificar si el proyecto existe
        if not Proyecto.objects.filter(id=proyecto_id).exists():
            return Response({"detail": "El proyecto no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener los usuarios asociados al proyecto
        usuario_proyectos = UsuarioProyecto.objects.filter(proyecto_id=proyecto_id)
        usuarios_ids = usuario_proyectos.values_list('usuario_id', flat=True)

        if not usuarios_ids:
            return Response({"detail": "No se encontraron usuarios para este proyecto."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener los datos corporales y datos personales de los usuarios asociados al proyecto
        datos = DatosCorporales.objects.filter(usuario_id__in=usuarios_ids, tipo='inicial').select_related('usuario')
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')

        if not datos.exists() or not datos_personales.exists():
            return Response({"detail": "No se encontraron datos corporales o personales para los usuarios del proyecto."}, status=status.HTTP_404_NOT_FOUND)

        # Crear un diccionario para acceder fácilmente al sexo de cada usuario
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

        for dato in datos:
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

        # Construir los resultados
        resultados = {}
        for clave, promedio in promedios.items():
            if clave in ['radio_abdominal', 'grasa_corporal', 'colesterol_hdl', 'porcentaje_musculo']:
                resultados[clave] = {
                    'M': {'promedio': promedio.get('M', None), 'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio.get('M', None), 'M')},
                    'F': {'promedio': promedio.get('F', None), 'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio.get('F', None), 'F')},
                }
            else:
                resultados[clave] = {
                    'promedio': promedio,
                    'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio) if promedio is not None else None
                }

        return Response(resultados, status=status.HTTP_200_OK)
