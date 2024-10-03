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
        except Usuario.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado',
                'data': {
                    'error': 'Usuario no encontrado'
                }
            }, status=status.HTTP_404_NOT_FOUND)

        if usuario.check_password(password):
            # Generar los tokens
            refresh = RefreshToken.for_user(usuario)

            # Devolver los tokens junto con el nombre, correo e id del usuario
            return Response({
                'success': True,
                'message': 'Inicio de sesión exitoso',
                'data': {
                    'id': usuario.id,  # Agregando el campo id
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'nombre': usuario.nombre,  # Asegúrate de que 'nombre' es un campo válido
                    'correo': usuario.correo,
                    'role': str(usuario.role)

                }
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Credenciales inválidas',
            'data': {
                'error': 'Credenciales inválidas'
            }
        }, status=status.HTTP_401_UNAUTHORIZED)


    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer