from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ...models.usuario_models import Usuario

from ..core.my_token_obtain_pair_serializer import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class LoginUsuarioView(APIView):
    def post(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')

        try:
            usuario = Usuario.objects.get(correo=correo)
            print(f"Usuario encontrado: {usuario}")
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if usuario.check_password(password):
            print("Contraseña válida")
            # Cambia aquí para usar la nueva vista de tokens
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        print("Contraseña inválida")
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer