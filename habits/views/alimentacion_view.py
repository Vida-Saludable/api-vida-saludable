from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from datetime import date

from ..models.alimentacion_model import Alimentacion
from ..serializers.alimentacion_serializer import AlimentacionSerializer
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario


class AlimentacionViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = AlimentacionSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        usuario = request.data.get('usuario')  # Obtener el usuario del request
        fecha = request.data.get('fecha', date.today())  # Obtener la fecha o usar la fecha actual

        # Verificar si ya existe un registro para el usuario en la fecha
        alimentacion_existente = Alimentacion.objects.filter(usuario=usuario, fecha=fecha).first()

        # Si existe un registro para esa fecha y usuario
        if alimentacion_existente:
            # Actualizar desayuno si está presente en el request
            if 'desayuno' in request.data:
                alimentacion_existente.desayuno = request.data.get('desayuno', alimentacion_existente.desayuno)
                alimentacion_existente.desayuno_hora = request.data.get('desayuno_hora', alimentacion_existente.desayuno_hora)
                alimentacion_existente.desayuno_saludable = request.data.get('desayuno_saludable', alimentacion_existente.desayuno_saludable)

            # Actualizar almuerzo si está presente en el request
            if 'almuerzo' in request.data:
                alimentacion_existente.almuerzo = request.data.get('almuerzo', alimentacion_existente.almuerzo)
                alimentacion_existente.almuerzo_hora = request.data.get('almuerzo_hora', alimentacion_existente.almuerzo_hora)
                alimentacion_existente.almuerzo_saludable = request.data.get('almuerzo_saludable', alimentacion_existente.almuerzo_saludable)

            # Actualizar cena si está presente en el request
            if 'cena' in request.data:
                alimentacion_existente.cena = request.data.get('cena', alimentacion_existente.cena)
                alimentacion_existente.cena_hora = request.data.get('cena_hora', alimentacion_existente.cena_hora)
                alimentacion_existente.cena_saludable = request.data.get('cena_saludable', alimentacion_existente.cena_saludable)
            
            alimentacion_existente.save()

            return Response({
                'success': True,
                'message': 'Se registró exitosamente',
                'data': AlimentacionSerializer(alimentacion_existente).data
            }, status=status.HTTP_200_OK)

        # Si no existe un registro, crear uno nuevo
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': True,
                'message': 'Se registró exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Modificar los datos para agregar nombres_apellidos y telefono del usuario
        for item in data:
            usuario_id = item['usuario']  # Obtener el id del usuario
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            if datos_personales:
                item['usuario'] = datos_personales.nombres_apellidos  # Reemplazar el ID con nombres_apellidos
                item['telefono'] = datos_personales.telefono  # Agregar el telefono
            else:
                item['usuario'] = None
                item['telefono'] = None

        return Response({
            'success': True,
            'message': 'Listado de registros de alimentación',
            'data': data
        })
