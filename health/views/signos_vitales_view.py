from rest_framework import viewsets

from health.models.signos_vitales_models import SignosVitales
from health.serializers.signos_vitales_serializer import SignosVitalesSerializer

class SignosVitalesViewSet(viewsets.ModelViewSet):
    queryset = SignosVitales.objects.all()
    serializer_class = SignosVitalesSerializer
    # permission_classes = [IsAuthenticated]
