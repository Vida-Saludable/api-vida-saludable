from django.db.models import F
import pandas as pd
from scipy.stats import pearsonr, spearmanr, kendalltau
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales
from habits.models.datos_habitos_agua_model import DatosHabitosAgua
from habits.models.datos_habitos_aire_model import DatosHabitosAire
from habits.models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion
from habits.models.datos_habitos_descanso_model import DatosHabitosDescanso
from habits.models.datos_habitos_ejercicio_model import DatosHabitosEjercicio
from habits.models.datos_habitos_esperanza_model import DatosHabitosEsperanza
from habits.models.datos_habitos_sol_model import DatosHabitosSol
from habits.models.datos_habitos_temperancia_model import DatosHabitosTemperancia

class CorrelationView(APIView):
    def get(self, request, *args, **kwargs):
        def get_datos(modelo, variable):
            return modelo.objects.filter(tipo=tipo_datos, usuario__isnull=False).values(variable, 'usuario')

        variable_x = request.GET.get('variable_x')
        variable_y = request.GET.get('variable_y')
        tipo_datos = request.GET.get('tipo', 'inicial')

        resultado_base = {
            "variable_x": variable_x,
            "variable_y": variable_y,
            "tipo": tipo_datos,
            "resultados": {
                "Pearson": {}, "Spearman": {}, "Kendall": {}
            }
        }

        if not variable_x or not variable_y:
            resultado_base["error"] = "Faltan parámetros 'variable_x' o 'variable_y'."
            return Response(resultado_base, status=status.HTTP_400_BAD_REQUEST)

        try:
            if variable_x in ['peso', 'altura', 'imc', 'radio_abdominal', 'grasa_corporal', 'grasa_visceral', 'porcentaje_musculo']:
                datos_corporales = get_datos(DatosFisicos, variable_x)
            elif variable_x in ['colesterol_total', 'colesterol_hdl', 'colesterol_ldl', 'trigliceridos', 'glucosa', 'glicemia_basal']:
                datos_corporales = get_datos(DatosMuestras, variable_x)
            elif variable_x in ['presion_sistolica', 'presion_diastolica', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura', 'saturacion_oxigeno']:
                datos_corporales = get_datos(SignosVitales, variable_x)
            else:
                raise ValueError("variable_x no corresponde a un modelo válido.")

            if variable_y in ['bebo_solo_agua_pura', 'bebo_8_vasos_agua', 'bebidas_con_azucar', 'bebo_agua_al_despertar', 'bebo_agua_antes_comidas', 'bebo_agua_para_dormir']:
                datos_habitos = get_datos(DatosHabitosAgua, variable_y)
            elif variable_y in ['tecnica_respiraciones_profundas', 'tiempo_tecnica_respiraciones', 'horario_tecnica_respiraciones_manana', 'horario_tecnica_respiraciones_noche']:
                datos_habitos = get_datos(DatosHabitosAire, variable_y)
            elif variable_y in ['consumo_3_comidas_horario_fijo', 'consumo_5_porciones_frutas_verduras', 'consumo_3_porciones_proteinas', 'ingiero_otros_alimentos', 'consumo_carbohidratos', 'consumo_alimentos_fritos', 'consumo_alimentos_hechos_en_casa', 'consumo_liquidos_mientras_como']:
                datos_habitos = get_datos(DatosHabitosAlimentacion, variable_y)
            elif variable_y in ['duermo_7_8_horas', 'despertar_durante_noche', 'dificultad_sueno_reparador', 'horario_sueno_diario', 'despertar_horario_diario']:
                datos_habitos = get_datos(DatosHabitosDescanso, variable_y)
            elif variable_y in ['realizo_actividad_deportiva', 'ejercicio_fisico_diario', 'practico_deporte_tiempo_libre', 'dedicacion_30_minutos_ejercicio', 'ejercicio_carrera_bicicleta']:
                datos_habitos = get_datos(DatosHabitosEjercicio, variable_y)
            elif variable_y in ['ser_supremo_interviene', 'leo_biblia', 'practico_oracion', 'orar_y_estudiar_biblia_desarrollo_personal']:
                datos_habitos = get_datos(DatosHabitosEsperanza, variable_y)
            elif variable_y in ['exposicion_sol_diaria', 'exposicion_sol_horas_seguras', 'exposicion_sol_20_minutos', 'uso_bloqueador_solar']:
                datos_habitos = get_datos(DatosHabitosSol, variable_y)
            elif variable_y in ['consumo_bebidas_alcoholicas', 'eventos_sociales_alcohol', 'consumo_sustancias_estimulantes', 'consumo_refrescos_cola', 'consumo_cigarrillos', 'consumo_comida_chatarra', 'pedir_mas_comida', 'agregar_mas_azucar', 'agregar_mas_sal', 'satisfecho_trabajo', 'tenso_nervioso_estresado', 'tiempo_libre_redes_sociales', 'satisfecho_relaciones_sociales', 'apoyo_familia_decisiones']:
                datos_habitos = get_datos(DatosHabitosTemperancia, variable_y)
            else:
                raise ValueError("variable_y no corresponde a un modelo válido.")

            df_corporales = pd.DataFrame(list(datos_corporales))
            df_habitos = pd.DataFrame(list(datos_habitos))

            if 'usuario' not in df_corporales.columns or 'usuario' not in df_habitos.columns:
                raise ValueError("Faltan datos de usuario para realizar la correlación.")

            x_total = len(df_corporales)
            y_total = len(df_habitos)

            x_valid = pd.to_numeric(df_corporales[variable_x], errors='coerce').notnull()
            y_valid = pd.to_numeric(df_habitos[variable_y], errors='coerce').notnull()

            datos_validos_x = int(x_valid.sum())
            datos_validos_y = int(y_valid.sum())

            df_corporales_valid = df_corporales[x_valid]
            df_habitos_valid = df_habitos[y_valid]

            df = pd.merge(df_corporales_valid, df_habitos_valid, on='usuario', how='inner')

            if df.empty or variable_x not in df.columns or variable_y not in df.columns:
                raise ValueError("No hay datos suficientes o no se encuentran las variables indicadas.")

            x_values = pd.to_numeric(df[variable_x], errors='coerce')
            y_values = pd.to_numeric(df[variable_y], errors='coerce')

            pares_validos = (~x_values.isnull() & ~y_values.isnull()).sum()

            detalles = {
                "registros_totales_x": x_total,
                "registros_totales_y": y_total,
                "datos_validos_x": datos_validos_x,
                "datos_validos_y": datos_validos_y,
                "pares_validos_para_correlacion": int(pares_validos)
            }

            if pares_validos < 2:
                resultado_base["error"] = "No hay suficientes datos válidos para realizar la correlación."
                resultado_base["detalles"] = detalles
                return Response(resultado_base, status=status.HTTP_400_BAD_REQUEST)

            def interpretar(corr, p, metodo):
                if pd.isna(corr) or pd.isna(p):
                    return "Datos insuficientes para calcular correlación."
                if p < 0.05:
                    intensidad = "fuerte" if abs(corr) >= 0.7 else "moderada" if abs(corr) >= 0.3 else "débil"
                    return f"**{metodo}**: Correlación de {corr:.2f}. Significativa (p={p:.3f}). Relación {intensidad}."
                else:
                    return f"**{metodo}**: No significativa (p={p:.3f}). Posible correlación por azar."

            pearson_corr, pearson_p = pearsonr(x_values, y_values)
            spearman_corr, spearman_p = spearmanr(x_values, y_values)
            kendall_corr, kendall_p = kendalltau(x_values, y_values)

            resultado_base["resultados"] = {
                "Pearson": {
                    "correlacion": pearson_corr,
                    "nivel_de_confiabilidad": pearson_p,
                    "interpretacion": interpretar(pearson_corr, pearson_p, "Pearson")
                },
                "Spearman": {
                    "correlacion": spearman_corr,
                    "nivel_de_confiabilidad": spearman_p,
                    "interpretacion": interpretar(spearman_corr, spearman_p, "Spearman")
                },
                "Kendall": {
                    "correlacion": kendall_corr,
                    "nivel_de_confiabilidad": kendall_p,
                    "interpretacion": interpretar(kendall_corr, kendall_p, "Kendall")
                },
            }
            resultado_base["detalles"] = detalles
            return Response(resultado_base, status=status.HTTP_200_OK)

        except Exception as e:
            resultado_base["error"] = str(e)
            return Response(resultado_base, status=status.HTTP_400_BAD_REQUEST)







# from django.db.models import F
# import pandas as pd
# from scipy.stats import pearsonr, spearmanr, kendalltau
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from health.models.datos_fisicos_models import DatosFisicos
# from health.models.datos_muestras_models import DatosMuestras
# from health.models.signos_vitales_models import SignosVitales
# from habits.models.datos_habitos_agua_model import DatosHabitosAgua
# from habits.models.datos_habitos_aire_model import DatosHabitosAire
# from habits.models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion
# from habits.models.datos_habitos_descanso_model import DatosHabitosDescanso
# from habits.models.datos_habitos_ejercicio_model import DatosHabitosEjercicio
# from habits.models.datos_habitos_esperanza_model import DatosHabitosEsperanza
# from habits.models.datos_habitos_sol_model import DatosHabitosSol
# from habits.models.datos_habitos_temperancia_model import DatosHabitosTemperancia

# class CorrelationView(APIView):
#     def get(self, request, *args, **kwargs):
#         variable_x = request.GET.get('variable_x')
#         variable_y = request.GET.get('variable_y')
#         tipo_datos = request.GET.get('tipo', 'inicial')  
#         if not variable_x or not variable_y:
#             return Response({"error": "Faltan parámetros 'variable_x' o 'variable_y'."}, status=status.HTTP_400_BAD_REQUEST)
#         if variable_x in ['peso', 'altura', 'imc', 'radio_abdominal', 'grasa_corporal', 'grasa_visceral', 'porcentaje_musculo']:
#             datos_corporales = DatosFisicos.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
#         elif variable_x in ['colesterol_total', 'colesterol_hdl', 'colesterol_ldl', 'trigliceridos', 'glucosa', 'glicemia_basal']:
#             datos_corporales = DatosMuestras.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
#         elif variable_x in ['presion_sistolica', 'presion_diastolica', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura', 'saturacion_oxigeno']:
#             datos_corporales = SignosVitales.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
  
#         else:
#             return Response({"error": "variable_x no corresponde a un modelo válido."}, status=status.HTTP_400_BAD_REQUEST)
#         if variable_y in ['bebo_solo_agua_pura', 'bebo_8_vasos_agua', 'bebidas_con_azucar', 'bebo_agua_al_despertar', 'bebo_agua_antes_comidas', 'bebo_agua_para_dormir']:
#             datos_habitos = DatosHabitosAgua.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['tecnica_respiraciones_profundas', 'tiempo_tecnica_respiraciones', 'horario_tecnica_respiraciones_manana', 'horario_tecnica_respiraciones_noche']:
#             datos_habitos = DatosHabitosAire.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['consumo_3_comidas_horario_fijo', 'consumo_5_porciones_frutas_verduras', 'consumo_3_porciones_proteinas', 'ingiero_otros_alimentos', 'consumo_carbohidratos', 'consumo_alimentos_fritos', 'consumo_alimentos_hechos_en_casa', 'consumo_liquidos_mientras_como']:
#             datos_habitos = DatosHabitosAlimentacion.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['duermo_7_8_horas', 'despertar_durante_noche', 'dificultad_sueno_reparador', 'horario_sueno_diario', 'despertar_horario_diario']:
#             datos_habitos = DatosHabitosDescanso.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['realizo_actividad_deportiva', 'ejercicio_fisico_diario', 'practico_deporte_tiempo_libre', 'dedicacion_30_minutos_ejercicio', 'ejercicio_carrera_bicicleta']:
#             datos_habitos = DatosHabitosEjercicio.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['ser_supremo_interviene', 'leo_biblia', 'practico_oracion', 'orar_y_estudiar_biblia_desarrollo_personal']:
#             datos_habitos = DatosHabitosEsperanza.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['exposicion_sol_diaria', 'exposicion_sol_horas_seguras', 'exposicion_sol_20_minutos', 'uso_bloqueador_solar']:
#             datos_habitos = DatosHabitosSol.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         elif variable_y in ['consumo_bebidas_alcoholicas', 'eventos_sociales_alcohol', 'consumo_sustancias_estimulantes', 'consumo_refrescos_cola', 'consumo_cigarrillos', 'consumo_comida_chatarra', 'pedir_mas_comida', 'agregar_mas_azucar', 'agregar_mas_sal', 'satisfecho_trabajo', 'tenso_nervioso_estresado', 'tiempo_libre_redes_sociales', 'satisfecho_relaciones_sociales', 'apoyo_familia_decisiones']:
#             datos_habitos = DatosHabitosTemperancia.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#         else:
#             return Response({"error": "variable_y no corresponde a un modelo válido."}, status=status.HTTP_400_BAD_REQUEST)
#         df_corporales = pd.DataFrame(list(datos_corporales))
#         df_habitos = pd.DataFrame(list(datos_habitos))

#         print("DF corporales columnas:", df_corporales.columns)
#         print("DF hábitos columnas:", df_habitos.columns)
#         df = pd.merge(df_corporales, df_habitos, on='usuario', how='inner')
#         if df.empty or len(df) < 2:
#             return Response({"error": "No hay suficientes datos para realizar la correlación."}, status=status.HTTP_400_BAD_REQUEST)
#         min_length = min(len(df[variable_x]), len(df[variable_y]))
#         x_values = df[variable_x].astype(float).iloc[:min_length]
#         y_values = df[variable_y].astype(float).iloc[:min_length]
#         try:
#             pearson_corr, pearson_p = pearsonr(x_values, y_values)
#             spearman_corr, spearman_p = spearmanr(x_values, y_values)
#             kendall_corr, kendall_p = kendalltau(x_values, y_values)
#         except Exception as e:
#             return Response({"error": f"Ocurrió un error al calcular las correlaciones: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#         def interpretar_correlaciones(correlation, p_value, method_name):
#             if p_value < 0.05:
#                 interpretation = f"**{method_name}**: Correlación de {correlation:.2f}. El valor p de {p_value:.3f} indica que esta correlación es significativa."
                
#                 if abs(correlation) >= 0.7:
#                     interpretation += " Esto indica una fuerte relación entre las variables."
#                 elif abs(correlation) >= 0.3:
#                     interpretation += " Esto indica una relación moderada entre las variables."
#                 else:
#                     interpretation += " Esto indica una relación débil entre las variables."
                
#                 return interpretation
#             else:
#                 return f"**{method_name}**: No hay una correlación significativa. El valor p de {p_value:.3f} sugiere que cualquier correlación observada podría ser producto del azar."
#         interpretaciones = {
#             "Pearson": interpretar_correlaciones(pearson_corr, pearson_p, "Pearson"),
#             "Spearman": interpretar_correlaciones(spearman_corr, spearman_p, "Spearman"),
#             "Kendall": interpretar_correlaciones(kendall_corr, kendall_p, "Kendall"),
#         }
#         return Response({
#              "variable_x": variable_x,
#             "variable_y": variable_y,
#              "tipo":tipo_datos ,
#             "resultados": {
#                 "Pearson": {
#                     "correlacion": pearson_corr,
#                     "valor_p": pearson_p,
#                     "interpretacion": interpretaciones["Pearson"],
#                 },
#                 "Spearman": {
#                     "correlacion": spearman_corr,
#                     "valor_p": spearman_p,
#                     "interpretacion": interpretaciones["Spearman"],
#                 },
#                 "Kendall": {
#                     "correlacion": kendall_corr,
#                     "valor_p": kendall_p,
#                     "interpretacion": interpretaciones["Kendall"],
#                 },
#             }
#         }, status=status.HTTP_200_OK)
