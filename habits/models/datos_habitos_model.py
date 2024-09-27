# from django.db import models

# from users.models.usuario_models import Usuario

# class DatosHabitos(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # ALIMENTACION
    # consumo_3_comidas_horario_fijo = models.IntegerField(null=True, blank=True)
    # consumo_5_porciones_frutas_verduras = models.IntegerField(null=True, blank=True)
    # consumo_3_porciones_proteinas = models.IntegerField(null=True, blank=True)
    # ingiero_otros_alimentos = models.IntegerField(null=True, blank=True)
    # consumo_carbohidratos = models.IntegerField(null=True, blank=True)
    # consumo_alimentos_fritos = models.IntegerField(null=True, blank=True)
    # consumo_alimentos_hechos_en_casa = models.IntegerField(null=True, blank=True)
    # consumo_liquidos_mientras_como = models.IntegerField(null=True, blank=True)

    # AGUA
    # bebo_solo_agua_pura = models.IntegerField(null=True, blank=True)
    # bebo_8_vasos_agua = models.IntegerField(null=True, blank=True)
    # bebidas_con_azucar = models.IntegerField(null=True, blank=True)
    # bebo_agua_al_despertar = models.IntegerField(null=True, blank=True)
    # bebo_agua_antes_comidas = models.IntegerField(null=True, blank=True)
    # bebo_agua_para_dormir = models.IntegerField(null=True, blank=True)

    # TEMPERANCIA
    # consumo_bebidas_alcoholicas = models.IntegerField(null=True, blank=True)
    # eventos_sociales_alcohol = models.IntegerField(null=True, blank=True)
    # consumo_sustancias_estimulantes = models.IntegerField(null=True, blank=True)
    # consumo_refrescos_cola = models.IntegerField(null=True, blank=True)
    # consumo_cigarrillos = models.IntegerField(null=True, blank=True)
    # consumo_comida_chatarra = models.IntegerField(null=True, blank=True)
    # pedir_mas_comida = models.IntegerField(null=True, blank=True)
    # agregar_mas_azucar = models.IntegerField(null=True, blank=True)
    # agregar_mas_sal = models.IntegerField(null=True, blank=True)
    # satisfecho_trabajo = models.IntegerField(null=True, blank=True)
    # tenso_nervioso_estresado = models.IntegerField(null=True, blank=True)
    # tiempo_libre_redes_sociales = models.IntegerField(null=True, blank=True)
    # satisfecho_relaciones_sociales = models.IntegerField(null=True, blank=True)
    # apoyo_familia_decisiones = models.IntegerField(null=True, blank=True)

    # EJERCICIO
    # realizo_actividad_deportiva = models.IntegerField(null=True, blank=True)
    # ejercicio_fisico_diario = models.IntegerField(null=True, blank=True)
    # practico_deporte_tiempo_libre = models.IntegerField(null=True, blank=True)
    # dedicacion_30_minutos_ejercicio = models.IntegerField(null=True, blank=True)
    # ejercicio_carrera_bicicleta = models.IntegerField(null=True, blank=True)

    # DESCANSO
    # duermo_7_8_horas = models.IntegerField(null=True, blank=True)
    # despertar_durante_noche = models.IntegerField(null=True, blank=True)
    # dificultad_sueno_reparador = models.IntegerField(null=True, blank=True)
    # horario_sueno_diario = models.IntegerField(null=True, blank=True)
    # despertar_horario_diario = models.IntegerField(null=True, blank=True)

    # LUZ SOLAR
    # exposicion_sol_diaria = models.IntegerField(null=True, blank=True)
    # exposicion_sol_horas_seguras = models.IntegerField(null=True, blank=True)
    # exposicion_sol_20_minutos = models.IntegerField(null=True, blank=True)
    # uso_bloqueador_solar = models.IntegerField(null=True, blank=True)

    # AIRE PURO
    # tecnica_respiraciones_profundas = models.IntegerField(null=True, blank=True)
    # tiempo_tecnica_respiraciones = models.IntegerField(null=True, blank=True)
    # horario_tecnica_respiraciones_manana = models.IntegerField(null=True, blank=True)
    # horario_tecnica_respiraciones_noche = models.IntegerField(null=True, blank=True)

    # ESPERANZA
    # ser_supremo_interviene = models.IntegerField(null=True, blank=True)
    # leo_biblia = models.IntegerField(null=True, blank=True)
    # practico_oracion = models.IntegerField(null=True, blank=True)
    # orar_y_estudiar_biblia_desarrollo_personal = models.IntegerField(null=True, blank=True)
    
    # tipo = models.CharField(max_length=20)  #inicial o final 

   

    # def __str__(self):
    #     return f"Hábitos de {self.usuario.correo}"