from rest_framework import viewsets

from .models import (
    Role, Usuario, DatosPersonalesUsuario, Alimentacion, Agua, Esperanza, Sol, Aire, Dormir,
    Despertar, Ejercicio, Proyecto, UsuarioProyecto, DatosCorporales, DatosHabitos
)
from .serializers import (
    RoleSerializer, UsuarioSerializer, DatosPersonalesUsuarioSerializer, AlimentacionSerializer, AguaSerializer, 
    EsperanzaSerializer, SolSerializer, AireSerializer, DormirSerializer, 
    DespertarSerializer, EjercicioSerializer, ProyectoSerializer, UsuarioProyectoSerializer,
    DatosCorporalesSerializer, DatosHabitosSerializer
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # permission_classes = [IsAuthenticated]



class DatosPersonalesUsuarioViewSet(viewsets.ModelViewSet):
    queryset = DatosPersonalesUsuario.objects.all()
    serializer_class = DatosPersonalesUsuarioSerializer
    # permission_classes = [IsAuthenticated]


class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # permission_classes = [IsAuthenticated]

class UsuarioProyectoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProyecto.objects.all()
    serializer_class = UsuarioProyectoSerializer
    # permission_classes = [IsAuthenticated]

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = AlimentacionSerializer
    # permission_classes = [IsAuthenticated]


class AguaViewSet(viewsets.ModelViewSet):
    queryset = Agua.objects.all()
    serializer_class = AguaSerializer
    # permission_classes = [IsAuthenticated]


class EsperanzaViewSet(viewsets.ModelViewSet):
    queryset = Esperanza.objects.all()
    serializer_class = EsperanzaSerializer
    # permission_classes = [IsAuthenticated]


class SolViewSet(viewsets.ModelViewSet):
    queryset = Sol.objects.all()
    serializer_class = SolSerializer
    # permission_classes = [IsAuthenticated]


class AireViewSet(viewsets.ModelViewSet):
    queryset = Aire.objects.all()
    serializer_class = AireSerializer
    # permission_classes = [IsAuthenticated]


class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
    # permission_classes = [IsAuthenticated]


class DespertarViewSet(viewsets.ModelViewSet):
    queryset = Despertar.objects.all()
    serializer_class = DespertarSerializer
    # permission_classes = [IsAuthenticated]


class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    # permission_classes = [IsAuthenticated]


class DatosCorporalesViewSet(viewsets.ModelViewSet):
    queryset = DatosCorporales.objects.all()
    serializer_class = DatosCorporalesSerializer
    # permission_classes = [IsAuthenticated]


class DatosHabitosViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitos.objects.all()
    serializer_class = DatosHabitosSerializer
    # permission_classes = [IsAuthenticated]