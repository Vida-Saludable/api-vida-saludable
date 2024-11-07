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
        # Obtén las variables a comparar desde los parámetros GET de la solicitud
        variable_x = request.GET.get('variable_x')
        variable_y = request.GET.get('variable_y')
        tipo_datos = request.GET.get('tipo', 'inicial')  # por defecto, toma los datos 'iniciales'

        # Verifica si ambos parámetros están presentes
        if not variable_x or not variable_y:
            return Response({"error": "Faltan parámetros 'variable_x' o 'variable_y'."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los datos en función del tipo y la variable_x
        if variable_x in ['peso', 'altura', 'imc', 'radio_abdominal', 'grasa_corporal', 'grasa_visceral', 'porcentaje_musculo']:
            datos_corporales = DatosFisicos.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
        elif variable_x in ['colesterol_total', 'colesterol_hdl', 'colesterol_ldl', 'trigliceridos', 'glucosa', 'glicemia_basal']:
            datos_corporales = DatosMuestras.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
        elif variable_x in ['presion_sistolica', 'presion_diastolica', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura', 'saturacion_oxigeno']:
            datos_corporales = SignosVitales.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
  
        else:
            return Response({"error": "variable_x no corresponde a un modelo válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar datos de hábitos en función de variable_y
        if variable_y in ['bebo_solo_agua_pura', 'bebo_8_vasos_agua', 'bebidas_con_azucar', 'bebo_agua_al_despertar', 'bebo_agua_antes_comidas', 'bebo_agua_para_dormir']:
            datos_habitos = DatosHabitosAgua.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['tecnica_respiraciones_profundas', 'tiempo_tecnica_respiraciones', 'horario_tecnica_respiraciones_manana', 'horario_tecnica_respiraciones_noche']:
            datos_habitos = DatosHabitosAire.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['consumo_3_comidas_horario_fijo', 'consumo_5_porciones_frutas_verduras', 'consumo_3_porciones_proteinas', 'ingiero_otros_alimentos', 'consumo_carbohidratos', 'consumo_alimentos_fritos', 'consumo_alimentos_hechos_en_casa', 'consumo_liquidos_mientras_como']:
            datos_habitos = DatosHabitosAlimentacion.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['duermo_7_8_horas', 'despertar_durante_noche', 'dificultad_sueno_reparador', 'horario_sueno_diario', 'despertar_horario_diario']:
            datos_habitos = DatosHabitosDescanso.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['realizo_actividad_deportiva', 'ejercicio_fisico_diario', 'practico_deporte_tiempo_libre', 'dedicacion_30_minutos_ejercicio', 'ejercicio_carrera_bicicleta']:
            datos_habitos = DatosHabitosEjercicio.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['ser_supremo_interviene', 'leo_biblia', 'practico_oracion', 'orar_y_estudiar_biblia_desarrollo_personal']:
            datos_habitos = DatosHabitosEsperanza.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['exposicion_sol_diaria', 'exposicion_sol_horas_seguras', 'exposicion_sol_20_minutos', 'uso_bloqueador_solar']:
            datos_habitos = DatosHabitosSol.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        elif variable_y in ['consumo_bebidas_alcoholicas', 'eventos_sociales_alcohol', 'consumo_sustancias_estimulantes', 'consumo_refrescos_cola', 'consumo_cigarrillos', 'consumo_comida_chatarra', 'pedir_mas_comida', 'agregar_mas_azucar', 'agregar_mas_sal', 'satisfecho_trabajo', 'tenso_nervioso_estresado', 'tiempo_libre_redes_sociales', 'satisfecho_relaciones_sociales', 'apoyo_familia_decisiones']:
            datos_habitos = DatosHabitosTemperancia.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        else:
            return Response({"error": "variable_y no corresponde a un modelo válido."}, status=status.HTTP_400_BAD_REQUEST)

        # Convierte los datos obtenidos en DataFrames
        df_corporales = pd.DataFrame(list(datos_corporales))
        df_habitos = pd.DataFrame(list(datos_habitos))

        # Fusiona los DataFrames en función del campo 'usuario'
        df = pd.merge(df_corporales, df_habitos, on='usuario', how='inner')

        # Verifica si hay suficientes datos para realizar la correlación
        if df.empty or len(df) < 2:
            return Response({"error": "No hay suficientes datos para realizar la correlación."}, status=status.HTTP_400_BAD_REQUEST)

        # Asegúrate de que ambos conjuntos de datos tengan la misma longitud
        min_length = min(len(df[variable_x]), len(df[variable_y]))
        x_values = df[variable_x].astype(float).iloc[:min_length]
        y_values = df[variable_y].astype(float).iloc[:min_length]

        # Calcula las correlaciones
        try:
            pearson_corr, pearson_p = pearsonr(x_values, y_values)
            spearman_corr, spearman_p = spearmanr(x_values, y_values)
            kendall_corr, kendall_p = kendalltau(x_values, y_values)
        except Exception as e:
            return Response({"error": f"Ocurrió un error al calcular las correlaciones: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Función para interpretar las correlaciones
        def interpretar_correlaciones(correlation, p_value, method_name):
            if p_value < 0.05:
                interpretation = f"**{method_name}**: Correlación de {correlation:.2f}. El valor p de {p_value:.3f} indica que esta correlación es significativa."
                
                if abs(correlation) >= 0.7:
                    interpretation += " Esto indica una fuerte relación entre las variables."
                elif abs(correlation) >= 0.3:
                    interpretation += " Esto indica una relación moderada entre las variables."
                else:
                    interpretation += " Esto indica una relación débil entre las variables."
                
                return interpretation
            else:
                return f"**{method_name}**: No hay una correlación significativa. El valor p de {p_value:.3f} sugiere que cualquier correlación observada podría ser producto del azar."

        # Genera las interpretaciones para cada tipo de correlación
        interpretaciones = {
            "Pearson": interpretar_correlaciones(pearson_corr, pearson_p, "Pearson"),
            "Spearman": interpretar_correlaciones(spearman_corr, spearman_p, "Spearman"),
            "Kendall": interpretar_correlaciones(kendall_corr, kendall_p, "Kendall"),
        }

        # Devuelve la respuesta con los resultados
        return Response({
             "variable_x": variable_x,
            "variable_y": variable_y,
             "tipo":tipo_datos ,
            "resultados": {
                "Pearson": {
                    "correlacion": pearson_corr,
                    "valor_p": pearson_p,
                    "interpretacion": interpretaciones["Pearson"],
                },
                "Spearman": {
                    "correlacion": spearman_corr,
                    "valor_p": spearman_p,
                    "interpretacion": interpretaciones["Spearman"],
                },
                "Kendall": {
                    "correlacion": kendall_corr,
                    "valor_p": kendall_p,
                    "interpretacion": interpretaciones["Kendall"],
                },
            }
        }, status=status.HTTP_200_OK)
