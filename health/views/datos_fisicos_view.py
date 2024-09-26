from rest_framework import viewsets

from health.models.datos_fisicos_models import DatosFisicos
from health.serializers.datos_fisicos_serializer import DatosFisicosSerializer

class DatosFisicosViewSet(viewsets.ModelViewSet):
    queryset = DatosFisicos.objects.all()
    serializer_class = DatosFisicosSerializer
    # permission_classes = [IsAuthenticated]
