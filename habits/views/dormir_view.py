from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from models.dormir_model import Dormir
from serializers.dormir_serializer import DormirSerializer


class DormirViewSet(viewsets.ModelViewSet):
    queryset = Dormir.objects.all()
    serializer_class = DormirSerializer
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