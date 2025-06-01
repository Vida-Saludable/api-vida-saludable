# import pandas as pd
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from habits.models.alimentacion_model import Alimentacion
# from habits.models.agua_model import Agua
# from habits.models.aire_model import Aire
# from habits.models.esperanza_model import Esperanza
# from habits.models.sol_model import Sol
# from habits.models.dormir_model import Dormir
# from habits.models.despertar_model import Despertar
# from habits.models.ejercicio_model import Ejercicio
# from .analizadorhabitos import AnalizadorHabitosVida

# class UserHabitsAllAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         usuario_id = self.kwargs.get('usuario_id')

#         try:
#             # Obtener los registros del usuario desde el primer día hasta el último registro
#             modelos = {
#                 'alimentacion': Alimentacion.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'agua': Agua.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'esperanza': Esperanza.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'sol': Sol.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'aire': Aire.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'dormir': Dormir.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'despertar': Despertar.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#                 'ejercicio': Ejercicio.objects.filter(usuario_id=usuario_id).order_by('fecha'),
#             }

#             # Verificar si los modelos tienen registros
#             if not all(len(modelo) for modelo in modelos.values()):
#                 return Response({'error': 'No hay suficientes datos en una o más categorías.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Encuentra el tamaño mínimo común para las listas
#             min_size = min(len(modelo) for modelo in modelos.values())

#             # Truncar los datos al tamaño mínimo común
#             for key in modelos:
#                 modelos[key] = list(modelos[key])[:min_size]

#             # Crear DataFrame con los datos clasificados y fechas formateadas
#             df = pd.DataFrame({
#                 'fecha': [data.fecha.strftime('%d-%m-%Y') for data in modelos['alimentacion']],  # Formatear la fecha
#                 'alimentacion': [
#                     AnalizadorHabitosVida.clasificar_alimentacion(
#                         data.desayuno, data.almuerzo, data.cena,
#                         getattr(data, 'desayuno_saludable', None), 
#                         getattr(data, 'almuerzo_saludable', None), 
#                         getattr(data, 'cena_saludable', None),
#                         getattr(data, 'desayuno_hora', None), 
#                         getattr(data, 'almuerzo_hora', None), 
#                         getattr(data, 'cena_hora', None)
#                     ) for data in modelos['alimentacion']
#                 ],
#                 'agua': [AnalizadorHabitosVida.clasificar_consumo_agua(data.cantidad) for data in modelos['agua']],
#                 'esperanza': [AnalizadorHabitosVida.clasificar_esperanza(data.tipo_practica) for data in modelos['esperanza']],
#                 'sol': [AnalizadorHabitosVida.clasificar_sol(data.tiempo) for data in modelos['sol']],
#                 'aire': [AnalizadorHabitosVida.clasificar_aire(data.tiempo) for data in modelos['aire']],
#                 'dormir': [
#                     AnalizadorHabitosVida.clasificar_sueno(data1.hora, data2.hora)
#                     for data1, data2 in zip(modelos['dormir'], modelos['despertar'])
#                 ],
#                 'ejercicio': [AnalizadorHabitosVida.clasificar_ejercicio(data.tipo, data.tiempo) for data in modelos['ejercicio']],
#             })

#         except KeyError as e:
#             return Response({'error': f"Campo faltante en el modelo: {e}"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Funciones de utilidad para analizar y generar recomendaciones
#         def calcular_tendencia(columna):
#             if df[columna].empty:
#                 return "No hay datos suficientes para calcular la tendencia."
#             tendencia = df[columna].iloc[-1] - df[columna].iloc[0]
#             if tendencia > 0:
#                 return f"El paciente está mejorando en {columna}."
#             elif tendencia < 0:
#                 return f"El paciente está empeorando en {columna}."
#             else:
#                 return f"El paciente se mantiene estable en {columna}."

#         def calcular_estadisticas(columna):
#             if df[columna].empty:
#                 return None, None, None
#             return df[columna].mean(), df[columna].median(), df[columna].std()

#         def comparar_con_normas(promedio, tipo):
#             normas = {
#                 'alimentacion': (70, 90),
#                 'agua': (2.0, 3.0),
#                 'esperanza': (75, 90),
#                 'sol': (30, 60),
#                 'aire': (0.5, 1.0),
#                 'dormir': (7, 9),
#                 'ejercicio': (150, 300),
#             }
#             rango = normas.get(tipo, (None, None))
#             if rango[0] is None:
#                 return "Norma no definida."
#             if promedio < rango[0]:
#                 return "Por debajo del rango recomendado."
#             elif promedio > rango[1]:
#                 return "Por encima del rango recomendado."
#             return "Dentro del rango recomendado."

#         def generar_recomendaciones(columna):
#             recomendaciones = []
#             promedio = df[columna].mean()
#             criterios = {
#                 'agua': (2.0, "Aumentar el consumo de agua para alcanzar el objetivo diario."),
#                 'alimentacion': (80, "Considerar ajustes en la dieta para mejorar la calidad de la alimentación."),
#                 'esperanza': (70, "Aumentar la frecuencia de prácticas de esperanza para mejorar el bienestar emocional."),
#                 'sol': (30, "Asegúrese de obtener al menos 30 minutos de exposición solar diaria."),
#                 'aire': (30, "Intente pasar al menos 30 minutos al aire libre diariamente."),
#                 'dormir': (7, "Intente dormir al menos 7-8 horas por noche."),
#                 'ejercicio': (150, "Aumente el tiempo de ejercicio a al menos 150 minutos semanales."),
#             }
#             if promedio < criterios[columna][0]:
#                 recomendaciones.append(criterios[columna][1])
#             return recomendaciones

#         def generar_alertas(columna):
#             alertas = []
#             std_dev = df[columna].std()
#             min_val = df[columna].min()

#             criterios_alertas = {
#                 'agua': (2.0, min_val, "El consumo de agua ha estado por debajo del objetivo."),
#                 'alimentacion': (10, std_dev, "La calidad de la alimentación ha sido inconsistente."),
#                 'esperanza': (10, std_dev, "La práctica de esperanza ha sido inconsistente."),
#                 'sol': (15, std_dev, "La exposición solar ha sido baja."),
#                 'aire': (15, std_dev, "La exposición al aire libre ha sido baja."),
#                 'dormir': (1.5, std_dev, "La calidad del sueño ha sido inconsistente."),
#                 'ejercicio': (30, std_dev, "El tiempo de ejercicio ha sido bajo."),
#             }

#             if std_dev and std_dev > criterios_alertas[columna][0]:
#                 alertas.append(criterios_alertas[columna][2])

#             return alertas

#         # Generar el resultado final con tendencia, estadísticas, recomendaciones y alertas
#         result = [
#             {
#                 'habito': habito,
#                 'tendencia': calcular_tendencia(habito),
#                 'promedio': calcular_estadisticas(habito)[0],
#                 'comparacion_normas': comparar_con_normas(calcular_estadisticas(habito)[0], habito),
#                 'recomendaciones': generar_recomendaciones(habito),
#                 'alertas': generar_alertas(habito),
#                 'historial': list(zip(df['fecha'], df[habito])),  # Incluir fechas en el historial
#             }
#             for habito in df.columns if habito != 'fecha'  # Excluir 'fecha' de los análisis
#         ]

#         return Response(result, status=status.HTTP_200_OK)




import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from habits.models.alimentacion_model import Alimentacion
from habits.models.agua_model import Agua
from habits.models.aire_model import Aire
from habits.models.esperanza_model import Esperanza
from habits.models.sol_model import Sol
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from habits.models.ejercicio_model import Ejercicio
from .analizadorhabitos import AnalizadorHabitosVida
from collections import defaultdict

class UserHabitsAllAPIView(APIView):
    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')
        try:
            fechas_set = set()
            registros = defaultdict(dict)

            def formatear_fecha(fecha):
                return fecha.strftime('%d-%m-%Y')

            def agregar_valores(modelos, campo, funcion):
                for modelo in modelos:
                    fecha_str = formatear_fecha(modelo.fecha)
                    registros[fecha_str][campo] = funcion(modelo)
                    fechas_set.add(fecha_str)
            agregar_valores(Alimentacion.objects.filter(usuario_id=usuario_id), 'alimentacion',
                            lambda d: AnalizadorHabitosVida.clasificar_alimentacion(
                                d.desayuno, d.almuerzo, d.cena,
                                getattr(d, 'desayuno_saludable', None), getattr(d, 'almuerzo_saludable', None), getattr(d, 'cena_saludable', None),
                                getattr(d, 'desayuno_hora', None), getattr(d, 'almuerzo_hora', None), getattr(d, 'cena_hora', None)))
            agregar_valores(Agua.objects.filter(usuario_id=usuario_id), 'agua',
                            lambda d: AnalizadorHabitosVida.clasificar_consumo_agua(d.cantidad))
            agregar_valores(Esperanza.objects.filter(usuario_id=usuario_id), 'esperanza',
                            lambda d: AnalizadorHabitosVida.clasificar_esperanza(d.tipo_practica))
            agregar_valores(Sol.objects.filter(usuario_id=usuario_id), 'sol',
                            lambda d: AnalizadorHabitosVida.clasificar_sol(d.tiempo))
            agregar_valores(Aire.objects.filter(usuario_id=usuario_id), 'aire',
                            lambda d: AnalizadorHabitosVida.clasificar_aire(d.tiempo))
            dormir_data = list(Dormir.objects.filter(usuario_id=usuario_id).order_by('fecha'))
            despertar_data = list(Despertar.objects.filter(usuario_id=usuario_id).order_by('fecha'))
            for d1, d2 in zip(dormir_data, despertar_data):
                fecha_str = formatear_fecha(d1.fecha)
                registros[fecha_str]['dormir'] = AnalizadorHabitosVida.clasificar_sueno(d1.hora, d2.hora)
                fechas_set.add(fecha_str)
            agregar_valores(Ejercicio.objects.filter(usuario_id=usuario_id), 'ejercicio',
                            lambda d: AnalizadorHabitosVida.clasificar_ejercicio(d.tipo, d.tiempo))

            fechas_ordenadas = sorted(fechas_set, key=lambda f: pd.to_datetime(f, format='%d-%m-%Y'))
            habitos = ['alimentacion', 'agua', 'esperanza', 'sol', 'aire', 'dormir', 'ejercicio']
            datos = {'fecha': fechas_ordenadas}
            for habito in habitos:
                datos[habito] = [registros[fecha].get(habito, 0) for fecha in fechas_ordenadas]

            df = pd.DataFrame(datos)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        def calcular_tendencia(columna):
            if df[columna].empty:
                return "No hay datos suficientes para calcular la tendencia."
            tendencia = df[columna].iloc[-1] - df[columna].iloc[0]
            if tendencia > 0:
                return f"El paciente está mejorando en {columna}."
            elif tendencia < 0:
                return f"El paciente está empeorando en {columna}."
            else:
                return f"El paciente se mantiene estable en {columna}."

        def calcular_estadisticas(columna):
            return df[columna].mean(), df[columna].median(), df[columna].std()

        def comparar_con_normas(promedio, tipo):
            normas = {
                'alimentacion': (70, 90),
                'agua': (2.0, 3.0),
                'esperanza': (75, 90),
                'sol': (30, 60),
                'aire': (0.5, 1.0),
                'dormir': (7, 9),
                'ejercicio': (150, 300),
            }
            rango = normas.get(tipo, (None, None))
            if promedio < rango[0]:
                return "Por debajo del rango recomendado."
            elif promedio > rango[1]:
                return "Por encima del rango recomendado."
            return "Dentro del rango recomendado."

        def generar_recomendaciones(columna):
            promedio = df[columna].mean()
            criterios = {
                'agua': (2.0, "Aumentar el consumo de agua para alcanzar el objetivo diario."),
                'alimentacion': (80, "Considerar ajustes en la dieta para mejorar la calidad de la alimentación."),
                'esperanza': (70, "Aumentar la frecuencia de prácticas de esperanza para mejorar el bienestar emocional."),
                'sol': (30, "Asegúrese de obtener al menos 30 minutos de exposición solar diaria."),
                'aire': (30, "Intente pasar al menos 30 minutos al aire libre diariamente."),
                'dormir': (7, "Intente dormir al menos 7-8 horas por noche."),
                'ejercicio': (150, "Aumente el tiempo de ejercicio a al menos 150 minutos semanales."),
            }
            if promedio < criterios[columna][0]:
                return [criterios[columna][1]]
            return []

        def generar_alertas(columna):
            std_dev = df[columna].std()
            criterios_alertas = {
                'agua': (2.0, "El consumo de agua ha estado por debajo del objetivo."),
                'alimentacion': (10, "La calidad de la alimentación ha sido inconsistente."),
                'esperanza': (10, "La práctica de esperanza ha sido inconsistente."),
                'sol': (15, "La exposición solar ha sido baja."),
                'aire': (15, "La exposición al aire libre ha sido baja."),
                'dormir': (1.5, "La calidad del sueño ha sido inconsistente."),
                'ejercicio': (30, "El tiempo de ejercicio ha sido bajo."),
            }
            if std_dev and std_dev > criterios_alertas[columna][0]:
                return [criterios_alertas[columna][1]]
            return []

        result = [
            {
                'habito': habito,
                'tendencia': calcular_tendencia(habito),
                'promedio': calcular_estadisticas(habito)[0],
                'comparacion_normas': comparar_con_normas(calcular_estadisticas(habito)[0], habito),
                'recomendaciones': generar_recomendaciones(habito),
                'alertas': generar_alertas(habito),
                'historial': list(zip(df['fecha'], df[habito])),
            }
            for habito in df.columns if habito != 'fecha'
        ]

        return Response(result, status=status.HTTP_200_OK)