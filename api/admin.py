from django.contrib import admin
from habits.models.agua_model import Agua
from habits.models.aire_model import Aire
from habits.models.alimentacion_model import Alimentacion
from habits.models.datos_habitos_agua_model import DatosHabitosAgua
from habits.models.datos_habitos_aire_model import DatosHabitosAire
from habits.models.datos_habitos_alimentacion_model import DatosHabitosAlimentacion
from habits.models.datos_habitos_descanso_model import DatosHabitosDescanso
from habits.models.datos_habitos_ejercicio_model import DatosHabitosEjercicio
from habits.models.datos_habitos_esperanza_model import DatosHabitosEsperanza
from habits.models.datos_habitos_sol_model import DatosHabitosSol
from habits.models.datos_habitos_temperancia_model import DatosHabitosTemperancia
from habits.models.esperanza_model import Esperanza
from habits.models.ejercicio_model import Ejercicio
from habits.models.sol_model import Sol
from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.proyecto_model import Proyecto
from users.models.role_model import Role
from users.models.usuario_proyecto_model import UsuarioProyecto
from health.models.datos_fisicos_models import DatosFisicos
from health.models.datos_muestras_models import DatosMuestras
from health.models.signos_vitales_models import SignosVitales
from health.models.test_ruffier_models import TestRuffier

admin.site.register(DatosPersonalesUsuario)
admin.site.register(Alimentacion)
admin.site.register(Agua)
admin.site.register(Esperanza)
admin.site.register(Sol)
admin.site.register(Aire)
admin.site.register(Role)
admin.site.register(Dormir)
admin.site.register(Despertar)
admin.site.register(Ejercicio)
admin.site.register(DatosFisicos)
admin.site.register(DatosMuestras)
admin.site.register(SignosVitales)
admin.site.register(TestRuffier)
admin.site.register(DatosHabitosAgua)
admin.site.register(DatosHabitosAire)
admin.site.register(DatosHabitosAlimentacion)
admin.site.register(DatosHabitosEjercicio)
admin.site.register(DatosHabitosTemperancia)
admin.site.register(DatosHabitosDescanso)
admin.site.register(DatosHabitosSol)
admin.site.register(DatosHabitosEsperanza)
admin.site.register(Proyecto)
admin.site.register(UsuarioProyecto)
