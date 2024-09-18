from rest_framework import viewsets

from health.models.datos_corporales_models import DatosCorporales
from health.serializers.datos_corporales_serializer import DatosCorporalesSerializer

class DatosCorporalesViewSet(viewsets.ModelViewSet):
    queryset = DatosCorporales.objects.all()
    serializer_class = DatosCorporalesSerializer
    # permission_classes = [IsAuthenticated]
