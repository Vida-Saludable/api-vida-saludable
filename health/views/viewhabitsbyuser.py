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

class HabitosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get('usuario_id')
        start_date = request.query_params.get('start_date', '2024-08-20')
        end_date = request.query_params.get('end_date', '2024-08-22')
        modelos = {
            'alimentacion': Alimentacion.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'agua': Agua.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'esperanza': Esperanza.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'sol': Sol.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'aire': Aire.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'dormir': Dormir.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'despertar': Despertar.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
            'ejercicio': Ejercicio.objects.filter(usuario_id=usuario_id, fecha__range=[start_date, end_date]),
        }
        datos_dict = {
            'alimentacion': [
                AnalizadorHabitosVida.clasificar_alimentacion(
                    data.desayuno, data.almuerzo, data.cena,
                    data.desayuno_saludable, data.almuerzo_saludable, data.cena_saludable,
                    data.desayuno_hora, data.almuerzo_hora, data.cena_hora
                ) for data in modelos['alimentacion']
            ],
            'agua': [AnalizadorHabitosVida.clasificar_consumo_agua(data.cantidad) for data in modelos['agua']],
            'esperanza': [AnalizadorHabitosVida.clasificar_esperanza(data.tipo_practica) for data in modelos['esperanza']],
            'sol': [AnalizadorHabitosVida.clasificar_sol(data.tiempo) for data in modelos['sol']],
            'aire': [AnalizadorHabitosVida.clasificar_aire(data.tiempo) for data in modelos['aire']],
            'dormir': [
                AnalizadorHabitosVida.clasificar_sueno(data1.hora, data2.hora)
                for data1, data2 in zip(modelos['dormir'], modelos['despertar'])
            ],
            'ejercicio': [AnalizadorHabitosVida.clasificar_ejercicio(data.tipo, data.tiempo) for data in modelos['ejercicio']],
        }
        
        def normalizar_con_ceros(diccionario):
            max_len = max(len(lista) for lista in diccionario.values())
            for clave in diccionario:
                diferencia = max_len - len(diccionario[clave])
                if diferencia > 0:
                    diccionario[clave].extend([0] * diferencia)
            return diccionario
        datos_dict = normalizar_con_ceros(datos_dict)
        df = pd.DataFrame(datos_dict)
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
            if df[columna].empty:
                return None, None, None
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
            if rango[0] is None:
                return "Norma no definida."
            if promedio < rango[0]:
                return "Por debajo del rango recomendado."
            elif promedio > rango[1]:
                return "Por encima del rango recomendado."
            return "Dentro del rango recomendado."

        def generar_recomendaciones(columna):
            recomendaciones = []
            promedio = df[columna].mean()
            criterios = {
                'agua': (2.0, "Aumentar el consumo de agua para alcanzar el objetivo diario."),
                'alimentacion': (80, "Considerar ajustes en la dieta para mejorar la calidad de la alimentación."),
                'esperanza': (70, "Aumentar la frecuencia de prácticas de esperanza para mejorar el bienestar emocional."),
                'sol': (30, "Asegúrese de obtener al menos 30 minutos de exposición solar diaria para mantener niveles adecuados de vitamina D."),
                'aire': (30, "Intente pasar al menos 30 minutos al aire libre diariamente para mejorar la calidad del aire que respira."),
                'dormir': (7, "Intente dormir al menos 7-8 horas por noche para mantener un buen estado de salud general."),
                'ejercicio': (150, "Aumente el tiempo de ejercicio a al menos 150 minutos semanales para mantener una buena salud cardiovascular."),
            }
            if promedio < criterios[columna][0]:
                recomendaciones.append(criterios[columna][1])
            return recomendaciones

        def generar_alertas(columna):
            alertas = []
            std_dev = df[columna].std()
            min_val = df[columna].min()

            criterios_alertas = {
                'agua': (2.0, min_val, "El consumo de agua ha estado por debajo del objetivo en algunos días."),
                'alimentacion': (10, std_dev, "La calidad de la alimentación ha sido inconsistente. Considere un ajuste en la dieta."),
                'esperanza': (10, std_dev, "La práctica de esperanza ha sido inconsistente. Considere aumentar la frecuencia."),
                'sol': (15, std_dev, "La exposición solar ha sido baja. Intente aumentar el tiempo al aire libre."),
                'aire': (15, std_dev, "La exposición al aire libre ha sido baja. Considere pasar más tiempo al exterior."),
                'dormir': (1.5, std_dev, "La calidad del sueño ha sido inconsistente. Considere evaluar sus hábitos de sueño."),
                'ejercicio': (30, std_dev, "El tiempo de ejercicio ha sido bajo. Intente incrementar la actividad física semanal."),
            }

            if std_dev and std_dev > criterios_alertas[columna][0]:
                alertas.append(criterios_alertas[columna][2])

            return alertas
        result = {
            habito: {
                'tendencia': calcular_tendencia(habito),
                'promedio': calcular_estadisticas(habito)[0],
                'historial': df[habito].tolist(),
                'comparacion_normas': comparar_con_normas(calcular_estadisticas(habito)[0], habito)
            }
            for habito in df.columns
        }

        result['recomendaciones'] = {habito: generar_recomendaciones(habito) for habito in df.columns}
        result['alertas'] = {habito: generar_alertas(habito) for habito in df.columns}

        return Response(result, status=status.HTTP_200_OK)
