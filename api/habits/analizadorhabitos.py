from decimal import Decimal
# from datetime import datetime, timedelta
from datetime import datetime, timedelta, time

class AnalizadorHabitosVida:
    
    @staticmethod
    def clasificar_alimentacion(desayuno, almuerzo, cena, desayuno_saludable, almuerzo_saludable, cena_saludable, hora_desayuno, hora_almuerzo, hora_cena):
        """
        Clasifica la calidad de la alimentación diaria, incluyendo la consideración de los horarios de las comidas.
        """
        # Horarios recomendados para las comidas (en formato 24 horas)
        hora_desayuno_recomendada = (time(6, 0), time(9, 0))  # 6:00 - 9:00 AM
        hora_almuerzo_recomendada = (time(12, 0), time(14, 0))  # 12:00 - 2:00 PM
        hora_cena_recomendada = (time(18, 0), time(20, 0))  # 6:00 - 8:00 PM

        puntaje = 0

        # Convertir las horas de comida a objetos time
        def convertir_a_time(hora):
            if isinstance(hora, int):
                return time(hora // 100, hora % 100)
            return hora

        hora_desayuno = convertir_a_time(hora_desayuno)
        hora_almuerzo = convertir_a_time(hora_almuerzo)
        hora_cena = convertir_a_time(hora_cena)

        # Desayuno
        if desayuno == 1:
            puntaje += 10
            if desayuno_saludable == 1:
                puntaje += 20
            if hora_desayuno_recomendada[0] <= hora_desayuno <= hora_desayuno_recomendada[1]:
                puntaje += 10
            else:
                puntaje -= 5  # Penalización por desayunar fuera del horario recomendado
        else:
            puntaje -= 10  # Penalización por saltarse el desayuno

        # Almuerzo
        if almuerzo == 1:
            puntaje += 10
            if almuerzo_saludable == 1:
                puntaje += 30
            if hora_almuerzo_recomendada[0] <= hora_almuerzo <= hora_almuerzo_recomendada[1]:
                puntaje += 10
            else:
                puntaje -= 5  # Penalización por almorzar fuera del horario recomendado
        else:
            puntaje -= 10  # Penalización por saltarse el almuerzo

        # Cena
        if cena == 1:
            puntaje += 10
            if cena_saludable == 1:
                puntaje += 20
            if hora_cena_recomendada[0] <= hora_cena <= hora_cena_recomendada[1]:
                puntaje += 10
            else:
                puntaje -= 5  # Penalización por cenar fuera del horario recomendado
        else:
            puntaje -= 10  # Penalización por saltarse la cena

        # Asegurar que el puntaje esté entre 0 y 100
        puntaje = max(0, min(puntaje, 100))

        return puntaje


    @staticmethod
    def clasificar_consumo_agua(cantidad):
        """
        Clasifica el consumo de agua en función de la cantidad ingerida en mililitros.
        """
        if cantidad >= 2500:
            return 100
        elif 2000 <= cantidad < 2500:
            return 90
        elif 1500 <= cantidad < 2000:
            return 70
        elif 1000 <= cantidad < 1500:
            return 50
        else:
            return 30



    @staticmethod
    def clasificar_esperanza(tipo_practica):
        """
        Clasifica la práctica espiritual según el tipo de actividad realizada.
        """
        if tipo_practica.lower() == 'oracion':
            return 90
        elif tipo_practica.lower() == 'biblia':
            return 100
        else:
            return 50


    @staticmethod
    def clasificar_sol(tiempo):
        """
        Clasifica la exposición al sol en función del tiempo en minutos.
        """
        if 15 <= tiempo <= 30:
            return 100
        elif 5 <= tiempo < 15 or 30 < tiempo <= 45:
            return 80
        else:
            return 50


    @staticmethod
    def clasificar_aire(tiempo):
        """
        Clasifica la exposición al aire fresco en función del tiempo en minutos.
        """
        if 20 <= tiempo <= 60:
            return 100
        elif 10 <= tiempo < 20 or 60 < tiempo <= 90:
            return 80
        else:
            return 50


    @staticmethod
    def clasificar_sueno(dormir_hora, despertar_hora):
        """
        Clasifica la calidad del sueño basándose en la cantidad de horas dormidas.
        """
        hoy = datetime.now().date()
        dormir_datetime = datetime.combine(hoy, dormir_hora)
        despertar_datetime = datetime.combine(hoy, despertar_hora)

        if despertar_datetime < dormir_datetime:
            despertar_datetime += timedelta(days=1)

        horas_dormidas = (despertar_datetime - dormir_datetime).seconds / 3600

        if 7 <= horas_dormidas <= 9:
            return 100
        elif 6 <= horas_dormidas < 7 or 9 < horas_dormidas <= 10:
            return 80
        elif 5 <= horas_dormidas < 6 or 10 < horas_dormidas <= 11:
            return 60
        else:
            return 40



    @staticmethod
    def clasificar_ejercicio(tipo, tiempo):
        """
        Clasifica el ejercicio en función del tipo y del tiempo en minutos.
        """
        if tipo.lower() == 'caminata lenta':
            return min(tiempo * 2, 100)
        elif tipo.lower() == 'caminata rapida':
            return min(tiempo * 2.5, 100)
        elif tipo.lower() == 'carrera':
            return min(tiempo * 3, 100)
        elif tipo.lower() == 'ejercicio guiado':
            return min(tiempo * 2, 100)
        else:
            return 50


    @staticmethod
    def calcular_puntaje_diario(alimentacion, agua, esperanza, sol, aire, sueno, despertar, ejercicio):
        puntajes = [
            AnalizadorHabitosVida.clasificar_alimentacion(
                alimentacion['desayuno'],
                alimentacion['almuerzo'],
                alimentacion['cena'],
                alimentacion['desayuno_saludable'],
                alimentacion['almuerzo_saludable'],
                alimentacion['cena_saludable']
            ),
            AnalizadorHabitosVida.clasificar_consumo_agua(agua['cantidad']),
            AnalizadorHabitosVida.clasificar_esperanza(esperanza['tipo_practica']),
            AnalizadorHabitosVida.clasificar_sol(sol['tiempo']),
            AnalizadorHabitosVida.clasificar_aire(aire['tiempo']),
            AnalizadorHabitosVida.clasificar_sueno(sueno['hora_dormir'], sueno['hora_despertar']),
            AnalizadorHabitosVida.clasificar_despertar(despertar['estado']),
            AnalizadorHabitosVida.clasificar_ejercicio(ejercicio['tipo'], ejercicio['tiempo'])
        ]
        
        puntaje_total = sum(puntajes) / len(puntajes)  # Promedio de puntajes sobre 100
        return puntaje_total  # Devuelve el puntaje total promedio sobre 100

