from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from models.sol_model import Sol
from serializers.sol_serializer import SolSerializer


class SolViewSet(viewsets.ModelViewSet):
    queryset = Sol.objects.all()
    serializer_class = SolSerializer
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