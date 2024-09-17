from django.contrib import admin
from .models import Role ,Usuario, Alimentacion, Agua, Esperanza, Sol, Aire, Dormir, Despertar, Ejercicio, DatosPersonalesUsuario, Proyecto, UsuarioProyecto, DatosCorporales, DatosHabitos

admin.site.register(Usuario)
admin.site.register(DatosPersonalesUsuario)
admin.site.register(Alimentacion)
admin.site.register(Agua)
admin.site.register(Esperanza)
admin.site.register(Sol)
admin.site.register(Aire)
admin.site.register(Dormir)
admin.site.register(Despertar)
admin.site.register(Ejercicio)
admin.site.register(DatosCorporales)
admin.site.register(DatosHabitos)
admin.site.register(Proyecto)
admin.site.register(UsuarioProyecto)
