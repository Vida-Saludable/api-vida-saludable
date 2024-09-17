from django.db.models import F
import pandas as pd
from scipy.stats import pearsonr, spearmanr, kendalltau
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import DatosCorporales, DatosHabitos

class CorrelationView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtén las variables a comparar desde los parámetros GET de la solicitud
        variable_x = request.GET.get('variable_x')
        variable_y = request.GET.get('variable_y')
        tipo_datos = request.GET.get('tipo', 'inicial')  # por defecto, toma los datos 'iniciales'

        # Verifica si ambos parámetros están presentes
        if not variable_x or not variable_y:
            return Response({"error": "Faltan parámetros 'variable_x' o 'variable_y'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtén los datos de las dos tablas en función de las variables proporcionadas y filtra por el tipo (inicial/final)
            datos_corporales = DatosCorporales.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
            datos_habitos = DatosHabitos.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
        except DatosCorporales.DoesNotExist:
            return Response({"error": "Datos corporales no encontrados."}, status=status.HTTP_404_NOT_FOUND)
        except DatosHabitos.DoesNotExist:
            return Response({"error": "Datos de hábitos no encontrados."}, status=status.HTTP_404_NOT_FOUND)

        # Convierte los datos obtenidos en DataFrames
        df_corporales = pd.DataFrame(list(datos_corporales))
        df_habitos = pd.DataFrame(list(datos_habitos))

        # Fusiona los DataFrames en función del campo 'usuario'
        df = pd.merge(df_corporales, df_habitos, on='usuario', how='inner')

        # Verifica si hay suficientes datos para realizar la correlación
        if df.empty or len(df) < 2:
            return Response({"error": "No hay suficientes datos para realizar la correlación."}, status=status.HTTP_400_BAD_REQUEST)

        # Extrae los valores de las variables y asegúrate de que sean numéricos
        x_values = df[variable_x].astype(float)
        y_values = df[variable_y].astype(float)

        # Calcula las correlaciones
        pearson_corr, pearson_p = pearsonr(x_values, y_values)
        spearman_corr, spearman_p = spearmanr(x_values, y_values)
        kendall_corr, kendall_p = kendalltau(x_values, y_values)

        # Función para interpretar las correlaciones
        def interpretar_correlaciones(correlation, p_value, method_name):
            if p_value < 0.05:
                interpretation = f"**{method_name}**: Correlación de {correlation:.2f}. El valor p de {p_value:.3f} indica que esta correlación es significativa."
                
                # Información adicional basada en el valor de la correlación
                if abs(correlation) >= 0.7:
                    interpretation += " Esto indica una fuerte relación entre las variables."
                elif abs(correlation) >= 0.3:
                    interpretation += " Esto indica una relación moderada entre las variables."
                else:
                    interpretation += " Esto indica una relación débil entre las variables."
                
                return interpretation
            else:
                return f"**{method_name}**: No hay una correlación significativa. El valor p de {p_value:.3f} sugiere que cualquier correlación observada podría ser producto del azar."

        # Almacena los resultados de las correlaciones en un diccionario
        correlations = {
            "pearson": {
                "correlation": pearson_corr,
                "p_value": pearson_p,
                "interpretacion": interpretar_correlaciones(pearson_corr, pearson_p, "Pearson")
            },
            "spearman": {
                "correlation": spearman_corr,
                "p_value": spearman_p,
                "interpretacion": interpretar_correlaciones(spearman_corr, spearman_p, "Spearman")
            },
            "kendall": {
                "correlation": kendall_corr,
                "p_value": kendall_p,
                "interpretacion": interpretar_correlaciones(kendall_corr, kendall_p, "Kendall")
            }
        }

        # Prepara los datos de la respuesta
        response_data = {
            "variable_x": variable_x,
            "variable_y": variable_y,
            "tipo": tipo_datos,  # Incluye el tipo en la respuesta
            "detailed_results": correlations
        }

        # Devuelve la respuesta con los datos de la correlación y la interpretación
        return Response(response_data, status=status.HTTP_200_OK)
