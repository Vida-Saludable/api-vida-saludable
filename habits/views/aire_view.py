from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.aire_model import Aire
from ..serializers.aire_serializer import AireSerializer


class AireViewSet(viewsets.ModelViewSet):
    queryset = Aire.objects.all()
    serializer_class = AireSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'success': True,
            'message': 'Se registro exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)