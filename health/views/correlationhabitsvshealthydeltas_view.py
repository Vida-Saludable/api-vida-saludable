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

class CorrelationHealthyVsHabitsDeltas(APIView):
    def get(self, request, *args, **kwargs):
        variable_x = request.GET.get('variable_x')
        variable_y = request.GET.get('variable_y')
        tipo_inicial = request.GET.get('tipo_inicial')
        tipo_final = request.GET.get('tipo_final')

        def get_datos(modelo, variable, tipo):
            return modelo.objects.filter(tipo=tipo, usuario__isnull=False).values(variable, 'usuario')

        def preparar_datos(variable, tipo, tipo_variable):
            if variable in ['peso', 'altura', 'imc', 'radio_abdominal', 'grasa_corporal', 'grasa_visceral', 'porcentaje_musculo']:
                return get_datos(DatosFisicos, variable, tipo)
            elif variable in ['colesterol_total', 'colesterol_hdl', 'colesterol_ldl', 'trigliceridos', 'glucosa', 'glicemia_basal']:
                return get_datos(DatosMuestras, variable, tipo)
            elif variable in ['presion_sistolica', 'presion_diastolica', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura', 'saturacion_oxigeno']:
                return get_datos(SignosVitales, variable, tipo)
            elif variable in ['bebo_solo_agua_pura', 'bebo_8_vasos_agua', 'bebidas_con_azucar', 'bebo_agua_al_despertar', 'bebo_agua_antes_comidas', 'bebo_agua_para_dormir']:
                return get_datos(DatosHabitosAgua, variable, tipo)
            elif variable in ['tecnica_respiraciones_profundas', 'tiempo_tecnica_respiraciones', 'horario_tecnica_respiraciones_manana', 'horario_tecnica_respiraciones_noche']:
                return get_datos(DatosHabitosAire, variable, tipo)
            elif variable in ['consumo_3_comidas_horario_fijo', 'consumo_5_porciones_frutas_verduras', 'consumo_3_porciones_proteinas', 'ingiero_otros_alimentos', 'consumo_carbohidratos', 'consumo_alimentos_fritos', 'consumo_alimentos_hechos_en_casa', 'consumo_liquidos_mientras_como']:
                return get_datos(DatosHabitosAlimentacion, variable, tipo)
            elif variable in ['duermo_7_8_horas', 'despertar_durante_noche', 'dificultad_sueno_reparador', 'horario_sueno_diario', 'despertar_horario_diario']:
                return get_datos(DatosHabitosDescanso, variable, tipo)
            elif variable in ['realizo_actividad_deportiva', 'ejercicio_fisico_diario', 'practico_deporte_tiempo_libre', 'dedicacion_30_minutos_ejercicio', 'ejercicio_carrera_bicicleta']:
                return get_datos(DatosHabitosEjercicio, variable, tipo)
            elif variable in ['ser_supremo_interviene', 'leo_biblia', 'practico_oracion', 'orar_y_estudiar_biblia_desarrollo_personal']:
                return get_datos(DatosHabitosEsperanza, variable, tipo)
            elif variable in ['exposicion_sol_diaria', 'exposicion_sol_horas_seguras', 'exposicion_sol_20_minutos', 'uso_bloqueador_solar']:
                return get_datos(DatosHabitosSol, variable, tipo)
            elif variable in ['consumo_bebidas_alcoholicas', 'eventos_sociales_alcohol', 'consumo_sustancias_estimulantes', 'consumo_refrescos_cola', 'consumo_cigarrillos', 'consumo_comida_chatarra', 'pedir_mas_comida', 'agregar_mas_azucar', 'agregar_mas_sal', 'satisfecho_trabajo', 'tenso_nervioso_estresado', 'tiempo_libre_redes_sociales', 'satisfecho_relaciones_sociales', 'apoyo_familia_decisiones']:
                return get_datos(DatosHabitosTemperancia, variable, tipo)
            else:
                raise ValueError(f"{tipo_variable} no corresponde a un modelo válido.")

        def calcular_correlacion(tipo):
            try:
                df_x = pd.DataFrame(list(preparar_datos(variable_x, tipo, 'variable_x')))
                df_y = pd.DataFrame(list(preparar_datos(variable_y, tipo, 'variable_y')))

                if 'usuario' not in df_x.columns or 'usuario' not in df_y.columns:
                    raise ValueError("Faltan datos de usuario para realizar la correlación.")

                total_x = len(df_x)
                total_y = len(df_y)
                valid_x = pd.to_numeric(df_x[variable_x], errors='coerce').notnull()
                valid_y = pd.to_numeric(df_y[variable_y], errors='coerce').notnull()

                datos_validos_x = int(valid_x.sum())
                datos_validos_y = int(valid_y.sum())

                df_x = df_x[valid_x]
                df_y = df_y[valid_y]

                df = pd.merge(df_x, df_y, on='usuario', how='inner')
                x_values = pd.to_numeric(df[variable_x], errors='coerce')
                y_values = pd.to_numeric(df[variable_y], errors='coerce')

                pares_validos = (~x_values.isnull() & ~y_values.isnull()).sum()

                if pares_validos < 2:
                    return None, {
                        "error": "No hay suficientes datos válidos para realizar la correlación.",
                        "detalles": {
                            "registros_totales_x": total_x,
                            "registros_totales_y": total_y,
                            "datos_validos_x": datos_validos_x,
                            "datos_validos_y": datos_validos_y,
                            "pares_validos_para_correlacion": pares_validos
                        }
                    }

                return {
                    "pearson": dict(zip(["correlation", "nivel_de_confiabilidad"], pearsonr(x_values, y_values))),
                    "spearman": dict(zip(["correlation", "nivel_de_confiabilidad"], spearmanr(x_values, y_values))),
                    "kendall": dict(zip(["correlation", "nivel_de_confiabilidad"], kendalltau(x_values, y_values))),
                    "detalles": {
                        "registros_totales_x": total_x,
                        "registros_totales_y": total_y,
                        "datos_validos_x": datos_validos_x,
                        "datos_validos_y": datos_validos_y,
                        "pares_validos_para_correlacion": pares_validos
                    }
                }, None
            except Exception as e:
                return None, {"error": str(e)}

        correlaciones_iniciales, error_i = calcular_correlacion(tipo_inicial)
        correlaciones_finales, error_f = calcular_correlacion(tipo_final)

        if error_i:
            return Response({
                "variable_x": variable_x,
                "variable_y": variable_y,
                "tipo_x": tipo_inicial,
                "tipo_y": tipo_final,
                "correlaciones_iniciales": {},
                "correlaciones_finales": {},
                "error": error_i["error"],
                "detalles": error_i.get("detalles", {})
            }, status=status.HTTP_400_BAD_REQUEST)

        if error_f:
            return Response({
                "variable_x": variable_x,
                "variable_y": variable_y,
                "tipo_x": tipo_inicial,
                "tipo_y": tipo_final,
                "correlaciones_iniciales": correlaciones_iniciales,
                "correlaciones_finales": {},
                "error": error_f["error"],
                "detalles": error_f.get("detalles", {})
            }, status=status.HTTP_400_BAD_REQUEST)

        def interpretar_cambio(cambio):
            if cambio > 0:
                return {
                    "interpretacion": "Aumento en la correlación.",
                    "cantidad_cambio": round(cambio, 3)
                }
            elif cambio < 0:
                return {
                    "interpretacion": "Disminución en la correlación.",
                    "cantidad_cambio": round(cambio, 3)
                }
            else:
                return {
                    "interpretacion": "Sin cambios en la correlación.",
                    "cantidad_cambio": 0
                }
        
        
        cambios = {
            "pearson": interpretar_cambio(correlaciones_finales["pearson"]["correlation"] - correlaciones_iniciales["pearson"]["correlation"]),
            "spearman": interpretar_cambio(correlaciones_finales["spearman"]["correlation"] - correlaciones_iniciales["spearman"]["correlation"]),
            "kendall": interpretar_cambio(correlaciones_finales["kendall"]["correlation"] - correlaciones_iniciales["kendall"]["correlation"]),
        }

        return Response({
            "variable_x": variable_x,
            "variable_y": variable_y,
            "tipo_x": tipo_inicial,
            "tipo_y": tipo_final,
            "correlaciones_iniciales": correlaciones_iniciales,
            "correlaciones_finales": correlaciones_finales,
            "cambios": cambios,
        }, status=status.HTTP_200_OK)

