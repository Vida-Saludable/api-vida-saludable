from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario 
from decimal import Decimal

class HealthIndicatorsComparisonAPIView(APIView):

    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')
        try:
            # Se obtiene los datos iniciales y finales de las distintas tablas
            datos_iniciales_fisicos = DatosFisicos.objects.get(usuario_id=usuario_id, tipo='inicial')
            datos_finales_fisicos = DatosFisicos.objects.get(usuario_id=usuario_id, tipo='final')
            
            datos_iniciales_muestras = DatosMuestras.objects.get(usuario_id=usuario_id, tipo='inicial')
            datos_finales_muestras = DatosMuestras.objects.get(usuario_id=usuario_id, tipo='final')
            
            datos_iniciales_signos = SignosVitales.objects.get(usuario_id=usuario_id, tipo='inicial')
            datos_finales_signos = SignosVitales.objects.get(usuario_id=usuario_id, tipo='final')
            


            datos_personales = DatosPersonalesUsuario.objects.get(usuario_id=usuario_id)

        except (DatosFisicos.DoesNotExist, DatosMuestras.DoesNotExist, SignosVitales.DoesNotExist):
            return Response({"detail": "Datos del usuario no encontrados."}, status=status.HTTP_404_NOT_FOUND)

        analisis_comparativo = self.realizar_comparacion(datos_iniciales_fisicos, datos_finales_fisicos,
                                                         datos_iniciales_muestras, datos_finales_muestras,
                                                         datos_iniciales_signos, datos_finales_signos, datos_personales)

        return Response(analisis_comparativo)

    def realizar_comparacion(self, datos_iniciales_fisicos, datos_finales_fisicos,
                             datos_iniciales_muestras, datos_finales_muestras,
                             datos_iniciales_signos, datos_finales_signos,
                           datos_personales):
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

        def validar_dato(valor):
            # Función para evitar valores nulos o vacíos
            if valor is None or valor == '':
                return None
            return valor

        def agregar_resultado(analisis, nombre, inicial, final, umbral_mejora, umbral_advertencia):
            inicial = validar_dato(inicial)
            final = validar_dato(final)
            if inicial is None or final is None:
                return

            mejora = calcular_mejora(inicial, final)
            recomendacion = generar_recomendacion(mejora, umbral_mejora, nombre)
            advertencia = generar_advertencia(inicial, final, nombre, umbral_advertencia)
            analisis[nombre] = {
                'valor_inicial': convertir_a_float(inicial),
                'valor_final': convertir_a_float(final),
                'diferencia': mejora,
                'recomendacion': recomendacion,
                'advertencia': advertencia
            }

        # Umbrales de mejora y advertencia (pueden ajustarse según criterios médicos)
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
  
        }

        # Indicadores de salud: DatosFisicos, DatosMuestras, SignosVitales, TestRuffier
        indicadores = [
            ('peso', datos_iniciales_fisicos.peso, datos_finales_fisicos.peso),
            ('altura', datos_iniciales_fisicos.altura, datos_finales_fisicos.altura),
            ('imc', datos_iniciales_fisicos.imc, datos_finales_fisicos.imc),
            ('presion_sistolica', datos_iniciales_signos.presion_sistolica, datos_finales_signos.presion_sistolica),
            ('presion_diastolica', datos_iniciales_signos.presion_diastolica, datos_finales_signos.presion_diastolica),
            ('radio_abdominal', datos_iniciales_fisicos.radio_abdominal, datos_finales_fisicos.radio_abdominal),
            ('grasa_corporal', datos_iniciales_fisicos.grasa_corporal, datos_finales_fisicos.grasa_corporal),
            ('grasa_visceral', datos_iniciales_fisicos.grasa_visceral, datos_finales_fisicos.grasa_visceral),
            ('frecuencia_cardiaca', datos_iniciales_signos.frecuencia_cardiaca, datos_finales_signos.frecuencia_cardiaca),
            ('frecuencia_respiratoria', datos_iniciales_signos.frecuencia_respiratoria, datos_finales_signos.frecuencia_respiratoria),
            ('colesterol_total', datos_iniciales_muestras.colesterol_total, datos_finales_muestras.colesterol_total),
            ('colesterol_hdl', datos_iniciales_muestras.colesterol_hdl, datos_finales_muestras.colesterol_hdl),
            ('colesterol_ldl', datos_iniciales_muestras.colesterol_ldl, datos_finales_muestras.colesterol_ldl),
            ('trigliceridos', datos_iniciales_muestras.trigliceridos, datos_finales_muestras.trigliceridos),
            ('glucosa', datos_iniciales_muestras.glucosa, datos_finales_muestras.glucosa),
            ('temperatura', datos_iniciales_signos.temperatura, datos_finales_signos.temperatura),
            ('saturacion_oxigeno', datos_iniciales_signos.saturacion_oxigeno, datos_finales_signos.saturacion_oxigeno),
            ('porcentaje_musculo', datos_iniciales_fisicos.porcentaje_musculo, datos_finales_fisicos.porcentaje_musculo),
            ('glicemia_basal', datos_iniciales_muestras.glicemia_basal, datos_finales_muestras.glicemia_basal),
      
        ]

       # Creación de una lista para almacenar los resultados del análisis
        analisis = []
        
        # Iteración por los indicadores, validando y calculando cada uno
        for nombre, inicial, final in indicadores:
            mejora = calcular_mejora(inicial, final)
            umbral_mejora = umbrales_mejora.get(nombre, 0)
            umbral_advertencia = umbrales_advertencia.get(nombre, 0)
            recomendacion = generar_recomendacion(mejora, umbral_mejora, nombre)
            advertencia = generar_advertencia(inicial, final, nombre, umbral_advertencia)
            
            # En lugar de añadir los datos a un diccionario, añádelos a la lista
            analisis.append({
                'nombre': nombre,
                'valor_inicial': convertir_a_float(inicial),
                'valor_final': convertir_a_float(final),
                'diferencia': mejora,
                'recomendacion': recomendacion,
                'advertencia': advertencia
            })
        
        # Devolvemos la lista de objetos
        return analisis
