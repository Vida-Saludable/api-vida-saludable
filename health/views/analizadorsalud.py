from decimal import Decimal

class AnalizadorSalud:
    
    @staticmethod
    def clasificar_peso(peso):
        if isinstance(peso, Decimal):
            peso = float(peso)
        if peso < Decimal(45):
            return 'Muy bajo'
        elif Decimal(45) <= peso < Decimal(60):
            return 'Bajo'
        elif Decimal(60) <= peso < Decimal(80):
            return 'Normal'
        elif Decimal(80) <= peso < Decimal(100):
            return 'Sobrepeso'
        else:
            return 'Obesidad'

    @staticmethod
    def clasificar_altura(altura):
        if Decimal('150') <= altura <= Decimal('190'):
            return 'Normal'
        else:
            return 'Fuera de rango normal'
    
    @staticmethod
    def calcular_imc(peso, altura):
        altura_metros = altura / Decimal('100')
        return peso / (altura_metros ** 2)
    
    @staticmethod
    def clasificar_imc(imc):
        if imc < Decimal('16'):
            return 'Muy bajo'
        elif Decimal('16') <= imc < Decimal('18.5'):
            return 'Bajo'
        elif Decimal('18.5') <= imc < Decimal('25'):
            return 'Normal'
        elif Decimal('25') <= imc < Decimal('30'):
            return 'Sobrepeso'
        else:
            return 'Obesidad'
    
    @staticmethod
    def clasificar_presion_sistolica(sistolica):
        if sistolica < 120:
            return 'Normal'
        elif 120 <= sistolica < 130:
            return 'Elevada'
        elif 130 <= sistolica < 140:
            return 'Hipertensión etapa 1'
        else:
            return 'Hipertensión etapa 2'

    @staticmethod
    def clasificar_presion_diastolica(diastolica):
        if diastolica < 80:
            return 'Normal'
        elif 80 <= diastolica < 90:
            return 'Hipertensión etapa 1'
        else:
            return 'Hipertensión etapa 2'

    @staticmethod
    def clasificar_radio_abdominal(radio_abdominal, sexo):
        if radio_abdominal is None:
            return 'Sin datos'

        if radio_abdominal > (Decimal('0.85') if sexo == 'F' else Decimal('0.9')):
            return 'Malo'
        else:
            return 'Bueno'


    @staticmethod
    def clasificar_grasa_corporal(grasa, sexo):
        if grasa is None:
            return 'Sin datos'
        if sexo == 'M':
            if grasa < 15:
                return 'Bajo'
            elif 15 <= grasa < 25:
                return 'Normal'
            else:
                return 'Alto'
        elif sexo == 'F':
            if grasa < 20:
                return 'Bajo'
            elif 20 <= grasa < 30:
                return 'Normal'
            else:
                return 'Alto'
        else:
            return 'Desconocido'

    @staticmethod
    def clasificar_grasa_visceral(grasa_visceral):
        if grasa_visceral > Decimal('13'):
            return 'Malo'
        elif Decimal('10') <= grasa_visceral <= Decimal('12'):
            return 'Aceptable'
        elif Decimal('7') <= grasa_visceral <= Decimal('9'):
            return 'Bueno'
        else:
            return 'Muy bueno'
    
    @staticmethod
    def clasificar_frecuencia_cardiaca(frecuencia_cardiaca):
        if frecuencia_cardiaca > 100:
            return 'Mala'
        elif 80 <= frecuencia_cardiaca <= 100:
            return 'Aceptable'
        elif 60 <= frecuencia_cardiaca <= 79:
            return 'Buena'
        else:
            return 'Muy buena'
    
    @staticmethod
    def clasificar_frecuencia_respiratoria(frecuencia_respiratoria):
        if frecuencia_respiratoria > 20:
            return 'Mala'
        elif 16 <= frecuencia_respiratoria <= 20:
            return 'Aceptable'
        elif 12 <= frecuencia_respiratoria <= 15:
            return 'Buena'
        else:
            return 'Muy buena'
    
    @staticmethod
    def clasificar_colesterol_total(colesterol_total):
        if colesterol_total > 240:
            return 'Malo'
        elif 200 <= colesterol_total <= 239:
            return 'Aceptable'
        else:
            return 'Bueno'

    @staticmethod
    def clasificar_colesterol_hdl(colesterol_hdl, sexo):
        if colesterol_hdl is None:
            return 'Sin datos'
        if colesterol_hdl < (40 if sexo == 'M' else 50):
            return 'Malo'
        else:
            return 'Bueno'
    
    @staticmethod
    def clasificar_colesterol_ldl(colesterol_ldl):
        if colesterol_ldl >= 160:
            return 'Malo'
        elif 130 <= colesterol_ldl <= 159:
            return 'Aceptable'
        elif 100 <= colesterol_ldl <= 129:
            return 'Bueno'
        else:
            return 'Muy bueno'

    @staticmethod
    def clasificar_trigliceridos(trigliceridos):
        if trigliceridos >= 200:
            return 'Malo'
        elif 150 <= trigliceridos < 200:
            return 'Aceptable'
        else:
            return 'Bueno'
    
    @staticmethod
    def clasificar_glucosa(glucosa):
        if glucosa >= 126:
            return 'Diabetes'
        elif 100 <= glucosa < 126:
            return 'Prediabetes'
        else:
            return 'Normal'
    
    @staticmethod
    def clasificar_frecuencia_cardiaca_en_reposo(frecuencia_cardiaca_reposo):
        if frecuencia_cardiaca_reposo > 100:
            return 'Mala'
        elif 80 <= frecuencia_cardiaca_reposo <= 100:
            return 'Aceptable'
        elif 60 <= frecuencia_cardiaca_reposo <= 79:
            return 'Buena'
        else:
            return 'Muy buena'
    
    @staticmethod
    def clasificar_frecuencia_cardiaca_despues_de_45_segundos(frecuencia_cardiaca_45_segundos):
        if frecuencia_cardiaca_45_segundos > 140:
            return 'Mala'
        elif 121 <= frecuencia_cardiaca_45_segundos <= 140:
            return 'Aceptable'
        elif 100 <= frecuencia_cardiaca_45_segundos <= 120:
            return 'Buena'
        else:
            return 'Muy buena'
    
    @staticmethod
    def clasificar_frecuencia_cardiaca_1_minuto_despues(frecuencia_cardiaca_1_minuto):
        if frecuencia_cardiaca_1_minuto > 100:
            return 'Mala'
        elif 80 <= frecuencia_cardiaca_1_minuto <= 100:
            return 'Aceptable'
        elif 60 <= frecuencia_cardiaca_1_minuto <= 79:
            return 'Buena'
        else:
            return 'Muy buena'
    
    @staticmethod
    def clasificar_resultado_test_rufier(resultados_test):

        if resultados_test > 15:
            return 'Muy malo'
        elif 11 <= resultados_test <= 14:
            return 'Malo'
        elif 6 <= resultados_test <= 10:
            return 'Aceptable'
        elif 0 <= resultados_test <= 5:
            return 'Bueno'
        else:  # resultados_test < 0
            return 'Excelente'
    
    # Métodos adicionales:
    
    @staticmethod
    def clasificar_temperatura(temperatura):
        if temperatura > 37.5:
            return 'Fiebre'
        elif 36.5 <= temperatura <= 37.5:
            return 'Normal'
        else:
            return 'Hipotermia'
    
    @staticmethod
    def clasificar_saturacion_oxigeno(saturacion_oxigeno):
        if saturacion_oxigeno < 90:
            return 'Bajo'
        elif 90 <= saturacion_oxigeno <= 95:
            return 'Aceptable'
        else:
            return 'Normal'
    
    @staticmethod
    def clasificar_porcentaje_musculo(porcentaje, sexo):
        # Implementa la lógica de clasificación aquí
        if porcentaje is None:
            return 'Sin datos'
        if sexo == 'M':
            if porcentaje < 40:
                return 'Bajo'
            elif 40 <= porcentaje < 50:
                return 'Normal'
            else:
                return 'Alto'
        elif sexo == 'F':
            if porcentaje < 30:
                return 'Bajo'
            elif 30 <= porcentaje < 40:
                return 'Normal'
            else:
                return 'Alto'
        else:
            return 'Desconocido'
    
    @staticmethod
    def clasificar_glicemia_basal(glicemia_basal):
        if glicemia_basal > 100:
            return 'Elevado'
        elif 70 <= glicemia_basal <= 100:
            return 'Normal'
        else:
            return 'Bajo'
    
    @staticmethod
    def clasificar_vitalidad(vitalidad):
        if vitalidad < 50:
            return 'Bajo'
        elif 50 <= vitalidad <= 75:
            return 'Normal'
        else:
            return 'Alto'
