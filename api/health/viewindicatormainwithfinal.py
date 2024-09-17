from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import DatosCorporales, DatosPersonalesUsuario
from .analizadorsalud import AnalizadorSalud
from decimal import Decimal

class HealthIndicatorsComparisonAPIView(APIView):

    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')
        try:
            datos_iniciales_corporales = DatosCorporales.objects.get(usuario_id=usuario_id, tipo='inicial')
            datos_finales_corporales = DatosCorporales.objects.get(usuario_id=usuario_id, tipo='final')
            datos_personales = DatosPersonalesUsuario.objects.get(usuario_id=usuario_id)
        except (DatosCorporales.DoesNotExist, DatosPersonalesUsuario.DoesNotExist):
            return Response({"detail": "Datos del usuario no encontrados."}, status=status.HTTP_404_NOT_FOUND)

        analisis_comparativo = self.realizar_comparacion(datos_iniciales_corporales, datos_finales_corporales, datos_personales)

        return Response(analisis_comparativo)

    def realizar_comparacion(self, datos_iniciales_corporales, datos_finales_corporales, datos_personales):
        analisis = {}

        def convertir_a_float(valor):
            if isinstance(valor, Decimal):
                return float(valor)
            try:
                return float(valor)
            except (ValueError, TypeError):
                return None

        def calcular_mejora(inicial, final):
            inicial = convertir_a_float(inicial)
            final = convertir_a_float(final)
            if inicial is None or final is None:
                return None
            return final - inicial

        def generar_recomendacion(mejora, umbral_mejora, indicador):
            if mejora is None:
                return f"Datos no válidos para {indicador}."
            if mejora > umbral_mejora:
                return f"Es necesario mejorar en {indicador}. Considera realizar cambios en tu estilo de vida."
            elif mejora < -umbral_mejora:
                return f"Se ha logrado una mejora significativa en {indicador}. ¡Continúa con el buen trabajo!"
            else:
                return f"El {indicador} se mantiene estable. Continúa monitoreando."

        def generar_advertencia(inicial, final, indicador, umbral_advertencia):
            inicial = convertir_a_float(inicial)
            final = convertir_a_float(final)
            if inicial is None or final is None:
                return f"Datos no disponibles para {indicador}."
            if final > inicial + umbral_advertencia:
                return f"{indicador} ha empeorado, es recomendable que consultes a un médico."
            elif final < inicial - umbral_advertencia:
                return f"{indicador} ha mejorado, sigue así."
            else:
                return f"{indicador} no ha mostrado cambios significativos."

        umbrales_mejora = {
            'peso': 5,
            'altura': 0.1,
            'imc': 1,
            'presion_sistolica': 10,
            'presion_diastolica': 5,
            'radio_abdominal': 5,
            'grasa_corporal': 2,
            'grasa_visceral': 2,
            'frecuencia_cardiaca': 10,
            'frecuencia_respiratoria': 2,
            'colesterol_total': 10,
            'colesterol_hdl': 5,
            'colesterol_ldl': 10,
            'trigliceridos': 10,
            'glucosa': 5,
            'temperatura': 0.2,
            'saturacion_oxigeno': 1,
            'porcentaje_musculo': 3,
            'glicemia_basal': 5,
            'frecuencia_cardiaca_en_reposo': 5,
            'frecuencia_cardiaca_despues_de_45_segundos': 10,
            'frecuencia_cardiaca_1_minuto_despues': 10,
            'resultado_test_rufier': 3,
        }

        umbrales_advertencia = {
            'peso': 2,
            'altura': 0.05,
            'imc': 0.5,
            'presion_sistolica': 5,
            'presion_diastolica': 3,
            'radio_abdominal': 2,
            'grasa_corporal': 1,
            'grasa_visceral': 1,
            'frecuencia_cardiaca': 5,
            'frecuencia_respiratoria': 1,
            'colesterol_total': 5,
            'colesterol_hdl': 3,
            'colesterol_ldl': 5,
            'trigliceridos': 5,
            'glucosa': 3,
            'temperatura': 0.1,
            'saturacion_oxigeno': 1,
            'porcentaje_musculo': 2,
            'glicemia_basal': 3,
            'frecuencia_cardiaca_en_reposo': 3,
            'frecuencia_cardiaca_despues_de_45_segundos': 5,
            'frecuencia_cardiaca_1_minuto_despues': 5,
            'resultado_test_rufier': 2,
        }

        indicadores = [
            ('peso', datos_iniciales_corporales.peso, datos_finales_corporales.peso),
            ('altura', datos_iniciales_corporales.altura, datos_finales_corporales.altura),
            ('imc', datos_iniciales_corporales.imc, datos_finales_corporales.imc),
            ('presion_sistolica', datos_iniciales_corporales.presion_sistolica, datos_finales_corporales.presion_sistolica),
            ('presion_diastolica', datos_iniciales_corporales.presion_diastolica, datos_finales_corporales.presion_diastolica),
            ('radio_abdominal', datos_iniciales_corporales.radio_abdominal, datos_finales_corporales.radio_abdominal),
            ('grasa_corporal', datos_iniciales_corporales.grasa_corporal, datos_finales_corporales.grasa_corporal),
            ('grasa_visceral', datos_iniciales_corporales.grasa_visceral, datos_finales_corporales.grasa_visceral),
            ('frecuencia_cardiaca', datos_iniciales_corporales.frecuencia_cardiaca, datos_finales_corporales.frecuencia_cardiaca),
            ('frecuencia_respiratoria', datos_iniciales_corporales.frecuencia_respiratoria, datos_finales_corporales.frecuencia_respiratoria),
            ('colesterol_total', datos_iniciales_corporales.colesterol_total, datos_finales_corporales.colesterol_total),
            ('colesterol_hdl', datos_iniciales_corporales.colesterol_hdl, datos_finales_corporales.colesterol_hdl),
            ('colesterol_ldl', datos_iniciales_corporales.colesterol_ldl, datos_finales_corporales.colesterol_ldl),
            ('trigliceridos', datos_iniciales_corporales.trigliceridos, datos_finales_corporales.trigliceridos),
            ('glucosa', datos_iniciales_corporales.glucosa, datos_finales_corporales.glucosa),
            ('temperatura', datos_iniciales_corporales.temperatura, datos_finales_corporales.temperatura),
            ('saturacion_oxigeno', datos_iniciales_corporales.saturacion_oxigeno, datos_finales_corporales.saturacion_oxigeno),
            ('porcentaje_musculo', datos_iniciales_corporales.porcentaje_musculo, datos_finales_corporales.porcentaje_musculo),
            ('glicemia_basal', datos_iniciales_corporales.glicemia_basal, datos_finales_corporales.glicemia_basal),
            ('frecuencia_cardiaca_en_reposo', datos_iniciales_corporales.frecuencia_cardiaca_en_reposo, datos_finales_corporales.frecuencia_cardiaca_en_reposo),
            ('frecuencia_cardiaca_despues_de_45_segundos', datos_iniciales_corporales.frecuencia_cardiaca_despues_de_45_segundos, datos_finales_corporales.frecuencia_cardiaca_despues_de_45_segundos),
            ('frecuencia_cardiaca_1_minuto_despues', datos_iniciales_corporales.frecuencia_cardiaca_1_minuto_despues, datos_finales_corporales.frecuencia_cardiaca_1_minuto_despues),
            ('resultado_test_rufier', datos_iniciales_corporales.resultado_test_rufier, datos_finales_corporales.resultado_test_rufier),
        ]

        for nombre, inicial, final in indicadores:
            mejora = calcular_mejora(inicial, final)
            umbral_mejora = umbrales_mejora.get(nombre, 0)
            umbral_advertencia = umbrales_advertencia.get(nombre, 0)
            recomendacion = generar_recomendacion(mejora, umbral_mejora, nombre)
            advertencia = generar_advertencia(inicial, final, nombre, umbral_advertencia)
            analisis[nombre] = {
                'valor_inicial': convertir_a_float(inicial),
                'valor_final': convertir_a_float(final),
                'diferencia': mejora,
                'recomendacion': recomendacion,
                'advertencia': advertencia
            }

        return analisis
