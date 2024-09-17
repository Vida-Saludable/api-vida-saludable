from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Usuario(models.Model):
    correo = models.EmailField(max_length=50, unique=True)
    contrasenia = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.correo


class DatosPersonalesUsuario(models.Model):
    nombres_apellidos = models.CharField(max_length=255, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    estado_civil = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    grado_instruccion = models.CharField(max_length=50, null=True, blank=True)
    procedencia = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.nombres_apellidos} - {self.usuario.correo}"


class Proyecto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.IntegerField()



    def __str__(self):
        return self.nombre


class UsuarioProyecto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('usuario', 'proyecto')

    def __str__(self):
        return f"{self.usuario} - {self.proyecto}"


class Alimentacion(models.Model):
    fecha = models.DateField()
    desayuno_hora = models.TimeField()
    almuerzo_hora = models.TimeField()
    cena_hora = models.TimeField()
    desayuno = models.IntegerField()  # Indica si hubo desayuno
    almuerzo = models.IntegerField()  # Indica si hubo almuerzo
    cena = models.IntegerField()      # Indica si hubo cena
    # Cambiar los campos de string a booleanos para indicar si fue saludable
    desayuno_saludable = models.IntegerField() 
    almuerzo_saludable = models.IntegerField()
    cena_saludable = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_alimento} ({self.fecha} {self.hora})"


class Agua(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad = models.IntegerField()  # En mililitros
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad}ml ({self.fecha} {self.hora})"


class Esperanza(models.Model):
    fecha = models.DateField()
    tipo_practica = models.CharField(max_length=50)  # oracion, leer la biblia
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo_practica} ({self.fecha})"


class Sol(models.Model):
    fecha = models.DateField()
    tiempo = models.IntegerField()  # Cantidad de minutos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tiempo} minutos ({self.fecha})"


class Aire(models.Model):
    fecha = models.DateField()
    tiempo = models.IntegerField()  # Cantidad de minutos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tiempo} minutos ({self.fecha})"


class Dormir(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sueño ({self.fecha} {self.hora})"
        


class Despertar(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Despertar ({self.fecha} {self.hora})"


class Ejercicio(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # caminata lenta, rápida, carrera, ejercicio guiado
    tiempo = models.IntegerField()  # Cantidad de minutos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ejercicio ({self.tipo} - {self.fecha})"


class DatosCorporales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    imc = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    presion_sistolica = models.IntegerField(null=True, blank=True)
    presion_diastolica = models.IntegerField(null=True, blank=True)
    radio_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grasa_visceral = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True)
    colesterol_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_hdl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    colesterol_ldl = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    trigliceridos = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    glucosa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    saturacion_oxigeno = models.IntegerField(null=True, blank=True)
    porcentaje_musculo = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    glicemia_basal = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    frecuencia_cardiaca_en_reposo = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_despues_de_45_segundos = models.IntegerField(null=True, blank=True)
    frecuencia_cardiaca_1_minuto_despues = models.IntegerField(null=True, blank=True)
    resultado_test_rufier = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)  #inicial o final 

    def __str__(self):
        return f"Datos corporales de {self.usuario.correo} ({self.tipo})"

class DatosHabitos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    consumo_3_comidas_horario_fijo = models.IntegerField(null=True, blank=True)
    consumo_5_porciones_frutas_verduras = models.IntegerField(null=True, blank=True)
    consumo_3_porciones_proteinas = models.IntegerField(null=True, blank=True)
    ingiero_otros_alimentos = models.IntegerField(null=True, blank=True)
    consumo_carbohidratos = models.IntegerField(null=True, blank=True)
    consumo_alimentos_fritos = models.IntegerField(null=True, blank=True)
    consumo_alimentos_hechos_en_casa = models.IntegerField(null=True, blank=True)
    consumo_liquidos_mientras_como = models.IntegerField(null=True, blank=True)
    bebo_solo_agua_pura = models.IntegerField(null=True, blank=True)
    bebo_8_vasos_agua = models.IntegerField(null=True, blank=True)
    bebidas_con_azucar = models.IntegerField(null=True, blank=True)
    bebo_agua_al_despertar = models.IntegerField(null=True, blank=True)
    bebo_agua_antes_comidas = models.IntegerField(null=True, blank=True)
    bebo_agua_para_dormir = models.IntegerField(null=True, blank=True)
    consumo_bebidas_alcoholicas = models.IntegerField(null=True, blank=True)
    eventos_sociales_alcohol = models.IntegerField(null=True, blank=True)
    consumo_sustancias_estimulantes = models.IntegerField(null=True, blank=True)
    consumo_refrescos_cola = models.IntegerField(null=True, blank=True)
    consumo_cigarrillos = models.IntegerField(null=True, blank=True)
    consumo_comida_chatarra = models.IntegerField(null=True, blank=True)
    pedir_mas_comida = models.IntegerField(null=True, blank=True)
    agregar_mas_azucar = models.IntegerField(null=True, blank=True)
    agregar_mas_sal = models.IntegerField(null=True, blank=True)
    satisfecho_trabajo = models.IntegerField(null=True, blank=True)
    tenso_nervioso_estresado = models.IntegerField(null=True, blank=True)
    tiempo_libre_redes_sociales = models.IntegerField(null=True, blank=True)
    satisfecho_relaciones_sociales = models.IntegerField(null=True, blank=True)
    apoyo_familia_decisiones = models.IntegerField(null=True, blank=True)
    realizo_actividad_deportiva = models.IntegerField(null=True, blank=True)
    ejercicio_fisico_diario = models.IntegerField(null=True, blank=True)
    practico_deporte_tiempo_libre = models.IntegerField(null=True, blank=True)
    dedicacion_30_minutos_ejercicio = models.IntegerField(null=True, blank=True)
    ejercicio_carrera_bicicleta = models.IntegerField(null=True, blank=True)
    duermo_7_8_horas = models.IntegerField(null=True, blank=True)
    despertar_durante_noche = models.IntegerField(null=True, blank=True)
    dificultad_sueno_reparador = models.IntegerField(null=True, blank=True)
    horario_sueno_diario = models.IntegerField(null=True, blank=True)
    despertar_horario_diario = models.IntegerField(null=True, blank=True)
    exposicion_sol_diaria = models.IntegerField(null=True, blank=True)
    exposicion_sol_horas_seguras = models.IntegerField(null=True, blank=True)
    exposicion_sol_20_minutos = models.IntegerField(null=True, blank=True)
    uso_bloqueador_solar = models.IntegerField(null=True, blank=True)
    tecnica_respiraciones_profundas = models.IntegerField(null=True, blank=True)
    tiempo_tecnica_respiraciones = models.IntegerField(null=True, blank=True)
    horario_tecnica_respiraciones_manana = models.IntegerField(null=True, blank=True)
    horario_tecnica_respiraciones_noche = models.IntegerField(null=True, blank=True)
    ser_supremo_interviene = models.IntegerField(null=True, blank=True)
    leo_biblia = models.IntegerField(null=True, blank=True)
    practico_oracion = models.IntegerField(null=True, blank=True)
    orar_y_estudiar_biblia_desarrollo_personal = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=20)  #inicial o final 

   

    def __str__(self):
        return f"Hábitos de {self.usuario.correo}"