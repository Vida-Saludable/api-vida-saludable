from rest_framework import viewsets

from health.models.test_ruffier_models import TestRuffier
from health.serializers.test_ruffier_serializer import TestRuffierSerializer

class TestRuffierViewSet(viewsets.ModelViewSet):
    queryset = TestRuffier.objects.all()
    serializer_class = TestRuffierSerializer
    # permission_classes = [IsAuthenticated]
