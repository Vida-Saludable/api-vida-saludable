from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from statistics import mean
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario 
from users.models.proyecto_model import Proyecto 
from users.models.usuario_proyecto_model import UsuarioProyecto 
from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales
from health.models.test_ruffier_models import TestRuffier
from .analizadorsalud import AnalizadorSalud

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

        # Obtener los datos de los 4 modelos y los datos personales de los usuarios asociados al proyecto
        datos_fisicos = DatosFisicos.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        datos_muestras = DatosMuestras.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        signos_vitales = SignosVitales.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        test_ruffier = TestRuffier.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')

        # Verificar si hay datos de salud disponibles
        if not (datos_fisicos.exists() or datos_muestras.exists() or signos_vitales.exists() or test_ruffier.exists()):
            return Response({"detail": "No se encontraron datos de salud para los usuarios del proyecto."}, status=status.HTTP_404_NOT_FOUND)

        # Crear un diccionario para acceder fácilmente al sexo de cada usuario
        sexo_usuario = {dato.usuario_id: dato.sexo for dato in datos_personales}

        # Inicializar acumuladores para los promedios de todos los indicadores de salud
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
            'resultado_test_ruffier': [],
        }

        # Llenar los indicadores con los datos de los diferentes modelos, ignorando datos nulos o inconsistentes
        for dato in datos_fisicos:
            usuario_id = dato.usuario_id
            sexo = sexo_usuario.get(usuario_id, 'M')
            if dato.peso is not None:
                indicadores['peso'].append(dato.peso)
            if dato.altura is not None:
                indicadores['altura'].append(dato.altura)
            if dato.imc is not None:
                indicadores['imc'].append(dato.imc)
            if dato.radio_abdominal is not None:
                indicadores['radio_abdominal'][sexo].append(dato.radio_abdominal)
            if dato.grasa_corporal is not None:
                indicadores['grasa_corporal'][sexo].append(dato.grasa_corporal)
            if dato.grasa_visceral is not None:
                indicadores['grasa_visceral'].append(dato.grasa_visceral)
            if dato.porcentaje_musculo is not None:
                indicadores['porcentaje_musculo'][sexo].append(dato.porcentaje_musculo)

        for dato in datos_muestras:
            usuario_id = dato.usuario_id
            sexo = sexo_usuario.get(usuario_id, 'M')
            if dato.colesterol_total is not None:
                indicadores['colesterol_total'].append(dato.colesterol_total)
            if dato.colesterol_hdl is not None:
                indicadores['colesterol_hdl'][sexo].append(dato.colesterol_hdl)
            if dato.colesterol_ldl is not None:
                indicadores['colesterol_ldl'].append(dato.colesterol_ldl)
            if dato.trigliceridos is not None:
                indicadores['trigliceridos'].append(dato.trigliceridos)
            if dato.glucosa is not None:
                indicadores['glucosa'].append(dato.glucosa)
            if dato.glicemia_basal is not None:
                indicadores['glicemia_basal'].append(dato.glicemia_basal)

        for dato in signos_vitales:
            if dato.frecuencia_cardiaca is not None:
                indicadores['frecuencia_cardiaca'].append(dato.frecuencia_cardiaca)
            if dato.temperatura is not None:
                indicadores['temperatura'].append(dato.temperatura)
            if dato.saturacion_oxigeno is not None:
                indicadores['saturacion_oxigeno'].append(dato.saturacion_oxigeno)
            if dato.frecuencia_respiratoria is not None:
                indicadores['frecuencia_respiratoria'].append(dato.frecuencia_respiratoria)
            if dato.presion_sistolica is not None:
                indicadores['presion_sistolica'].append(dato.presion_sistolica)
            if dato.presion_diastolica is not None:
                indicadores['presion_diastolica'].append(dato.presion_diastolica)

        for dato in test_ruffier:
            if dato.frecuencia_cardiaca_en_reposo is not None:
                indicadores['frecuencia_cardiaca_en_reposo'].append(dato.frecuencia_cardiaca_en_reposo)
            if dato.frecuencia_cardiaca_despues_de_45_segundos is not None:
                indicadores['frecuencia_cardiaca_despues_de_45_segundos'].append(dato.frecuencia_cardiaca_despues_de_45_segundos)
            if dato.frecuencia_cardiaca_1_minuto_despues is not None:
                indicadores['frecuencia_cardiaca_1_minuto_despues'].append(dato.frecuencia_cardiaca_1_minuto_despues)
            if dato.resultado_test_ruffier is not None:
                indicadores['resultado_test_ruffier'].append(dato.resultado_test_ruffier)

        # Calcular el promedio de cada indicador
        promedios = {}
        for clave, valores in indicadores.items():
            if isinstance(valores, dict):
                promedios[clave] = {}
                for subclave, subvalores in valores.items():
                    # Calcular el promedio solo si hay valores
                    promedios[clave][subclave] = mean(subvalores) if subvalores else None
            else:
                # Calcular el promedio solo si hay valores
                promedios[clave] = mean(valores) if valores else None

        # Construir los resultados con los análisis
        resultados = {}
        for clave, promedio in promedios.items():
            if clave in ['radio_abdominal', 'grasa_corporal', 'colesterol_hdl', 'porcentaje_musculo']:
                resultados[clave] = {
                    'M': {'promedio': promedio.get('M', None), 'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio.get('M', None), 'M') if promedio.get('M', None) is not None else None},
                    'F': {'promedio': promedio.get('F', None), 'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio.get('F', None), 'F') if promedio.get('F', None) is not None else None},
                }
            else:
                resultados[clave] = {
                    'promedio': promedio,
                    'status': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio) if promedio is not None else None
                }

        return Response(resultados, status=status.HTTP_200_OK)
