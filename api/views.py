from rest_framework import status
from rest_framework import viewsets


from .models import (
    Role, Usuario, DatosPersonalesUsuario, Alimentacion, Agua, Esperanza, Sol, Aire, Dormir,
    Despertar, Ejercicio, Proyecto, UsuarioProyecto, DatosCorporales, DatosHabitos
)
from .serializers import (
    RoleSerializer, UsuarioSerializer, DatosPersonalesUsuarioSerializer, AlimentacionSerializer, AguaSerializer, 
    EsperanzaSerializer, SolSerializer, AireSerializer, DormirSerializer, 
    DespertarSerializer, EjercicioSerializer, ProyectoSerializer, UsuarioProyectoSerializer,
    DatosCorporalesSerializer, DatosHabitosSerializer
)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer


from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer




class DatosPersonalesUsuarioViewSet(viewsets.ModelViewSet):
    queryset = DatosPersonalesUsuario.objects.all()
    serializer_class = DatosPersonalesUsuarioSerializer
    permission_classes = [IsAuthenticated]

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "success": True,
            "message": "Proyecto registrado correctamente",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "success": True,
            "message": "Proyecto actualizado correctamente",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        instance = serializer.save()
        estado = serializer.validated_data.get('estado')
        if estado is not None:
            instance.estado = estado
        instance.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "success": True,
            "message": "Proyecto eliminado correctamente"
        }, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

class UsuarioProyectoViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProyecto.objects.all()
    serializer_class = UsuarioProyectoSerializer
    # permission_classes = [IsAuthenticated]

class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = AlimentacionSerializer
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

class EsperanzaViewSet(viewsets.ModelViewSet):
    queryset = Esperanza.objects.all()
    serializer_class = EsperanzaSerializer
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


class DespertarViewSet(viewsets.ModelViewSet):
    queryset = Despertar.objects.all()
    serializer_class = DespertarSerializer
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


class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
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


class DatosCorporalesViewSet(viewsets.ModelViewSet):
    queryset = DatosCorporales.objects.all()
    serializer_class = DatosCorporalesSerializer
    # permission_classes = [IsAuthenticated]


class DatosHabitosViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitos.objects.all()
    serializer_class = DatosHabitosSerializer
    # permission_classes = [IsAuthenticated]



#################################################################################3
#auth


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class LogoutUsuarioView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)