from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from rest_framework.views import APIView

from ..models.datos_habitos_esperanza_model import DatosHabitosEsperanza
from ..serializers.datos_habitos_esperanza_serializer import DatosHabitosEsperanzaSerializer


class DatosHabitosEsperanzaViewSet(viewsets.ModelViewSet):
    queryset = DatosHabitosEsperanza.objects.all()
    serializer_class = DatosHabitosEsperanzaSerializer

    def create(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario')  # Asegúrate de que el campo 'usuario' está presente en los datos

        # Verificar si hay registros previos del mismo usuario
        registros_previos = DatosHabitosEsperanza.objects.filter(usuario_id=usuario_id).order_by('-fecha')

        with transaction.atomic():  # Para asegurar que las actualizaciones sean atómicas
            if not registros_previos.exists():
                # Si no hay registros previos, el tipo será 'inicial'
                request.data['tipo'] = 'inicial'
            else:
                ultimo_registro = registros_previos.first()

                if ultimo_registro.tipo == 'inicial':
                    # Si el último registro es 'inicial', este nuevo será 'final'
                    request.data['tipo'] = 'final'
                elif ultimo_registro.tipo == 'final':
                    # Si el último registro es 'final', actualizamos ese registro a 'seguimiento'
                    ultimo_registro.tipo = 'seguimiento'
                    ultimo_registro.save()

                    # El nuevo registro será 'final'
                    request.data['tipo'] = 'final'
                else:
                    # Si el último registro es 'seguimiento', el nuevo registro será 'final'
                    request.data['tipo'] = 'final'

            # Crear el nuevo registro
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Datos que se devolverán con el mensaje de éxito
                response_data = {
                    "success": True,  # Indicador de éxito
                    "message": "Registro de esperanza creado con éxito.",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "success": False,
                    "message": "Error al crear el registro de esperanza.",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
class ListaDatosHabitosEsperanzaUsuarioView(APIView):
    def get(self, request, usuario_id, *args, **kwargs):
        # Filtrar los registros de hábitos de esperanza por el usuario recibido en la URL
        registros = DatosHabitosEsperanza.objects.filter(usuario_id=usuario_id)

        if not registros.exists():
            return Response({
                "success": False,
                "message": "No se encontraron registros de hábitos de esperanza para este usuario."
            }, status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos
        serializer = DatosHabitosEsperanzaSerializer(registros, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)