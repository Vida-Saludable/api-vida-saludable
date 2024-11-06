from decimal import Decimal

class AnalizadorSalud:
    
    @staticmethod
    def clasificar_peso(peso):
        if isinstance(peso, Decimal):
            peso = float(peso)
        if peso < Decimal(45):
            return {'status': 'Muy bajo', 'color': '#FF4C4C'}  # Rojo
        elif Decimal(45) <= peso < Decimal(60):
            return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
        elif Decimal(60) <= peso < Decimal(80):
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        elif Decimal(80) <= peso < Decimal(100):
            return {'status': 'Sobrepeso', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Obesidad', 'color': '#FF0000'}  # Rojo oscuro

    @staticmethod
    def clasificar_altura(altura):
        if Decimal('150') <= altura <= Decimal('190'):
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Fuera de rango normal', 'color': '#FFA500'}  # Naranja
        
    @staticmethod
    def clasificar_imc(imc):
        if imc < Decimal('16'):
            return {'status': 'Muy bajo', 'color': '#FF4C4C'}  # Rojo
        elif Decimal('16') <= imc < Decimal('18.5'):
            return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
        elif Decimal('18.5') <= imc < Decimal('25'):
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        elif Decimal('25') <= imc < Decimal('30'):
            return {'status': 'Sobrepeso', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Obesidad', 'color': '#FF0000'}  # Rojo oscuro

    @staticmethod
    def clasificar_presion_sistolica(sistolica):
        if sistolica < 120:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        elif 120 <= sistolica < 130:
            return {'status': 'Elevada', 'color': '#FFD700'}  # Amarillo
        elif 130 <= sistolica < 140:
            return {'status': 'Hipertensión etapa 1', 'color': '#FFA500'}  # Naranja
        else:
            return {'status': 'Hipertensión etapa 2', 'color': '#FF0000'}  # Rojo oscuro
        

    @staticmethod
    def clasificar_presion_diastolica(diastolica):
        if diastolica < 80:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        elif 80 <= diastolica < 90:
            return {'status': 'Hipertensión etapa 1', 'color': '#FFA500'}  # Naranja
        else:
            return {'status': 'Hipertensión etapa 2', 'color': '#FF0000'}  # Rojo oscuro

    @staticmethod
    def clasificar_radio_abdominal(radio_abdominal, sexo):
        if radio_abdominal is None:
            return {'status': 'Sin datos', 'color': '#D3D3D3'}  # Gris
        if radio_abdominal > (Decimal('0.85') if sexo == 'F' else Decimal('0.9')):
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        else:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde
        
    @staticmethod
    def clasificar_grasa_corporal(grasa, sexo):
        if grasa is None:
            return {'status': 'Sin datos', 'color': '#D3D3D3'}  # Gris
        if sexo == 'M':
            if grasa < 15:
                return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
            elif 15 <= grasa < 25:
                return {'status': 'Normal', 'color': '#00FF00'}  # Verde
            else:
                return {'status': 'Alto', 'color': '#FF4C4C'}  # Rojo
        elif sexo == 'F':
            if grasa < 20:
                return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
            elif 20 <= grasa < 30:
                return {'status': 'Normal', 'color': '#00FF00'}  # Verde
            else:
                return {'status': 'Alto', 'color': '#FF4C4C'}  # Rojo

    @staticmethod
    def clasificar_grasa_visceral(grasa_visceral):
        if grasa_visceral > Decimal('13'):
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        elif Decimal('10') <= grasa_visceral <= Decimal('12'):
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif Decimal('7') <= grasa_visceral <= Decimal('9'):
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy bueno', 'color': '#32CD32'}  # Verde claro
        
    
    @staticmethod
    def clasificar_frecuencia_cardiaca(frecuencia_cardiaca):
        if frecuencia_cardiaca > 100:
            return {'status': 'Mala', 'color': '#FF4C4C'}  # Rojo
        elif 80 <= frecuencia_cardiaca <= 100:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 60 <= frecuencia_cardiaca <= 79:
            return {'status': 'Buena', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy buena', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_frecuencia_respiratoria(frecuencia_respiratoria):
        if frecuencia_respiratoria > 20:
            return {'status': 'Mala', 'color': '#FF4C4C'}  # Rojo
        elif 16 <= frecuencia_respiratoria <= 20:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 12 <= frecuencia_respiratoria <= 15:
            return {'status': 'Buena', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy buena', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_colesterol_total(colesterol_total):
        if colesterol_total > 240:
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        elif 200 <= colesterol_total <= 239:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde

    @staticmethod
    def clasificar_colesterol_hdl(colesterol_hdl, sexo):
        if colesterol_hdl is None:
            return {'status': 'Sin datos', 'color': '#D3D3D3'}  # Gris
        if colesterol_hdl < (40 if sexo == 'M' else 50):
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        else:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde

    @staticmethod
    def clasificar_colesterol_ldl(colesterol_ldl):
        if colesterol_ldl >= 160:
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        elif 130 <= colesterol_ldl <= 159:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 100 <= colesterol_ldl <= 129:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy bueno', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_trigliceridos(trigliceridos):
        if trigliceridos >= 200:
            return {'status': 'Malo', 'color': '#FF4C4C'}  # Rojo
        elif 150 <= trigliceridos < 200:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde
        

    @staticmethod
    def clasificar_glucosa(glucosa):
        if glucosa >= 126:
            return {'status': 'Diabetes', 'color': '#FF4C4C'}  # Rojo
        elif 100 <= glucosa < 126:
            return {'status': 'Prediabetes', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde

    @staticmethod
    def clasificar_frecuencia_cardiaca_en_reposo(frecuencia_cardiaca_reposo):
        if frecuencia_cardiaca_reposo > 100:
            return {'status': 'Mala', 'color': '#FF4C4C'}  # Rojo
        elif 80 <= frecuencia_cardiaca_reposo <= 100:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 60 <= frecuencia_cardiaca_reposo <= 79:
            return {'status': 'Buena', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy buena', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_frecuencia_cardiaca_despues_de_45_segundos(frecuencia_cardiaca_45_segundos):
        if frecuencia_cardiaca_45_segundos > 140:
            return {'status': 'Mala', 'color': '#FF4C4C'}  # Rojo
        elif 121 <= frecuencia_cardiaca_45_segundos <= 140:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 100 <= frecuencia_cardiaca_45_segundos <= 120:
            return {'status': 'Buena', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy buena', 'color': '#32CD32'}  # Verde claro
        
    @staticmethod
    def clasificar_frecuencia_cardiaca_1_minuto_despues(frecuencia_cardiaca_1_minuto):
        if frecuencia_cardiaca_1_minuto > 100:
            return {'status': 'Mala', 'color': '#FF4C4C'}  # Rojo
        elif 80 <= frecuencia_cardiaca_1_minuto <= 100:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 60 <= frecuencia_cardiaca_1_minuto <= 79:
            return {'status': 'Buena', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Muy buena', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_resultado_test_ruffier(resultados_test):
        if resultados_test > 15:
            return {'status': 'Muy malo', 'color': '#FF4C4C'}  # Rojo
        elif 11 <= resultados_test <= 14:
            return {'status': 'Malo', 'color': '#FFA500'}  # Naranja
        elif 6 <= resultados_test <= 10:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        elif 0 <= resultados_test <= 5:
            return {'status': 'Bueno', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Excelente', 'color': '#32CD32'}  # Verde claro

    @staticmethod
    def clasificar_temperatura(temperatura):
        if temperatura > 37.5:
            return {'status': 'Fiebre', 'color': '#FF4C4C'}  # Rojo
        elif 36.5 <= temperatura <= 37.5:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Hipotermia', 'color': '#FFA500'}  # Naranja
        
    @staticmethod
    def clasificar_saturacion_oxigeno(saturacion_oxigeno):
        if saturacion_oxigeno < 90:
            return {'status': 'Bajo', 'color': '#FF4C4C'}  # Rojo
        elif 90 <= saturacion_oxigeno <= 95:
            return {'status': 'Aceptable', 'color': '#FFD700'}  # Amarillo
        else:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde

    @staticmethod
    def clasificar_porcentaje_musculo(porcentaje, sexo):
        if porcentaje is None:
            return {'status': 'Sin datos', 'color': '#D3D3D3'}  # Gris
        if sexo == 'M':
            if porcentaje < 40:
                return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
            elif 40 <= porcentaje < 50:
                return {'status': 'Normal', 'color': '#00FF00'}  # Verde
            else:
                return {'status': 'Alto', 'color': '#FF4C4C'}  # Rojo
        elif sexo == 'F':
            if porcentaje < 30:
                return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
            elif 30 <= porcentaje < 40:
                return {'status': 'Normal', 'color': '#00FF00'}  # Verde
            else:
                return {'status': 'Alto', 'color': '#FF4C4C'}  # Rojo

    @staticmethod
    def clasificar_glicemia_basal(glicemia_basal):
        if glicemia_basal > 100:
            return {'status': 'Elevado', 'color': '#FF4C4C'}  # Rojo
        elif 70 <= glicemia_basal <= 100:
            return {'status': 'Normal', 'color': '#00FF00'}  # Verde
        else:
            return {'status': 'Bajo', 'color': '#FFA500'}  # Naranja
