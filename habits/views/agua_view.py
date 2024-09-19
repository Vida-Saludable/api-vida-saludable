from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.agua_model import Agua
from serializers.agua_serializer import AguaSerializer


class AguaViewSet(viewsets.ModelViewSet):
    queryset = Agua.objects.all()
    serializer_class = AguaSerializer
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