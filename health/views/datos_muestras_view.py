from rest_framework import viewsets

from health.models.datos_muestras_models import DatosMuestras
from health.serializers.datos_muestras_serializer import DatosMuestrasSerializer

class DatosMuestrasViewSet(viewsets.ModelViewSet):
    queryset = DatosMuestras.objects.all()
    serializer_class = DatosMuestrasSerializer
    # permission_classes = [IsAuthenticated]
