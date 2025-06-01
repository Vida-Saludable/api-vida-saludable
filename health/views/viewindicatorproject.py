from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from statistics import mean
from decimal import Decimal, ROUND_HALF_UP
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario 
from users.models.proyecto_model import Proyecto 
from users.models.usuario_proyecto_model import UsuarioProyecto 
from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales

from .analizadorsalud import AnalizadorSalud

class IndicadoresSaludPorProyectoView(APIView):

    def get(self, request, proyecto_id, *args, **kwargs):

        if not Proyecto.objects.filter(id=proyecto_id).exists():
            return Response({"detail": "El proyecto no existe."}, status=status.HTTP_404_NOT_FOUND)
        usuario_proyectos = UsuarioProyecto.objects.filter(proyecto_id=proyecto_id)
        usuarios_ids = usuario_proyectos.values_list('usuario_id', flat=True)

        if not usuarios_ids:
            return Response({"detail": "No se encontraron usuarios para este proyecto."}, status=status.HTTP_404_NOT_FOUND)
        datos_fisicos = DatosFisicos.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        datos_muestras = DatosMuestras.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        signos_vitales = SignosVitales.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id__in=usuarios_ids).select_related('usuario')
        if not (datos_fisicos.exists() or datos_muestras.exists() or signos_vitales.exists()):
            return Response({"detail": "No se encontraron datos de salud para los usuarios del proyecto."}, status=status.HTTP_404_NOT_FOUND)
        sexo_usuario = {dato.usuario_id: dato.sexo for dato in datos_personales}
        indicadores = {
            'peso': [], 'altura': [], 'imc': [], 'radio_abdominal': {'M': [], 'F': []},
            'porcentaje_musculo': {'M': [], 'F': []}, 'grasa_corporal': {'M': [], 'F': []},
            'grasa_visceral': [], 'colesterol_total': [], 'colesterol_hdl': {'M': [], 'F': []},
            'colesterol_ldl': [], 'trigliceridos': [], 'glucosa': [], 'presion_sistolica': [],
            'presion_diastolica': [], 'frecuencia_cardiaca': [], 'frecuencia_respiratoria': [],
            'saturacion_oxigeno': [], 'glicemia_basal': [], 'temperatura': []
        }
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
            if dato.porcentaje_musculo is not None:
                indicadores['porcentaje_musculo'][sexo].append(dato.porcentaje_musculo)
            if dato.grasa_corporal is not None:
                indicadores['grasa_corporal'][sexo].append(dato.grasa_corporal)
            if dato.grasa_visceral is not None:
                indicadores['grasa_visceral'].append(dato.grasa_visceral)

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
            if dato.frecuencia_respiratoria is not None:
                indicadores['frecuencia_respiratoria'].append(dato.frecuencia_respiratoria)
            if dato.presion_sistolica is not None:
                indicadores['presion_sistolica'].append(dato.presion_sistolica)
            if dato.presion_diastolica is not None:
                indicadores['presion_diastolica'].append(dato.presion_diastolica)
            if dato.saturacion_oxigeno is not None:
                indicadores['saturacion_oxigeno'].append(dato.saturacion_oxigeno)
            if dato.temperatura is not None:
                indicadores['temperatura'].append(dato.temperatura)

        def redondear(valor):
            return float(Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        promedios = {}
        for clave, valores in indicadores.items():
            if isinstance(valores, dict):
                promedios[clave] = {}
                for subclave, subvalores in valores.items():
                    promedios[clave][subclave] = redondear(mean(subvalores)) if subvalores else None
            else:
                promedios[clave] = redondear(mean(valores)) if valores else None

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
                    'data': getattr(AnalizadorSalud, f'clasificar_{clave}')(promedio) if promedio is not None else None
                }

        return Response(resultados, status=status.HTTP_200_OK)
