# from django.db.models import F
# import pandas as pd
# from scipy.stats import pearsonr, spearmanr, kendalltau
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from ..models.datos_corporales_models import DatosCorporales
# from habits.models.datos_habitos_model import DatosHabitos

# class CorrelationHealthyVsHabitsDeltas(APIView):
#     def get(self, request, *args, **kwargs):
#         variable_x = request.GET.get('variable_x')
#         variable_y = request.GET.get('variable_y')

#         if not variable_x or not variable_y:
#             return Response({"error": "Faltan parámetros 'variable_x' o 'variable_y'."}, status=status.HTTP_400_BAD_REQUEST)

#         def obtener_correlaciones(tipo_datos):
#             try:
#                 datos_corporales = DatosCorporales.objects.filter(tipo=tipo_datos).values(variable_x, 'usuario')
#                 datos_habitos = DatosHabitos.objects.filter(tipo=tipo_datos).values(variable_y, 'usuario')
#             except (DatosCorporales.DoesNotExist, DatosHabitos.DoesNotExist):
#                 return None, Response({"error": f"Datos no encontrados para {tipo_datos}."}, status=status.HTTP_404_NOT_FOUND)

#             df_corporales = pd.DataFrame(list(datos_corporales))
#             df_habitos = pd.DataFrame(list(datos_habitos))

#             df = pd.merge(df_corporales, df_habitos, on='usuario', how='inner')

#             if df.empty or len(df) < 2:
#                 return None, Response({"error": f"No hay suficientes datos para realizar la correlación ({tipo_datos})."}, status=status.HTTP_400_BAD_REQUEST)

#             x_values = df[variable_x].astype(float)
#             y_values = df[variable_y].astype(float)

#             pearson_corr, pearson_p = pearsonr(x_values, y_values)
#             spearman_corr, spearman_p = spearmanr(x_values, y_values)
#             kendall_corr, kendall_p = kendalltau(x_values, y_values)

#             return {
#                 "pearson": {"correlation": pearson_corr, "p_value": pearson_p},
#                 "spearman": {"correlation": spearman_corr, "p_value": spearman_p},
#                 "kendall": {"correlation": kendall_corr, "p_value": kendall_p},
#             }, None

#         correlaciones_iniciales, error_iniciales = obtener_correlaciones('inicial')
#         correlaciones_finales, error_finales = obtener_correlaciones('final')

#         if error_iniciales:
#             return error_iniciales
#         if error_finales:
#             return error_finales

#         if not correlaciones_iniciales or not correlaciones_finales:
#             return Response({"error": "No se pudieron obtener todas las correlaciones."}, status=status.HTTP_400_BAD_REQUEST)

#         def interpretar_cambio(cambio):
#             if cambio > 0:
#                 return "Aumento en la correlación."
#             elif cambio < 0:
#                 return "Disminución en la correlación."
#             else:
#                 return "No hay cambio en la correlación."

#         response_data = {
#             "variable_x": variable_x,
#             "variable_y": variable_y,
#             "inicial_correlations": correlaciones_iniciales,
#             "final_correlations": correlaciones_finales,
#             "correlation_changes": {
#                 "pearson": {
#                     "change": correlaciones_finales['pearson']['correlation'] - correlaciones_iniciales['pearson']['correlation'],
#                     "interpretation": interpretar_cambio(correlaciones_finales['pearson']['correlation'] - correlaciones_iniciales['pearson']['correlation']),
#                 },
#                 "spearman": {
#                     "change": correlaciones_finales['spearman']['correlation'] - correlaciones_iniciales['spearman']['correlation'],
#                     "interpretation": interpretar_cambio(correlaciones_finales['spearman']['correlation'] - correlaciones_iniciales['spearman']['correlation']),
#                 },
#                 "kendall": {
#                     "change": correlaciones_finales['kendall']['correlation'] - correlaciones_iniciales['kendall']['correlation'],
#                     "interpretation": interpretar_cambio(correlaciones_finales['kendall']['correlation'] - correlaciones_iniciales['kendall']['correlation']),
#                 }
#             }
#         }

#         return Response(response_data, status=status.HTTP_200_OK)

