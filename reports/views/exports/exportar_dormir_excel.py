import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from datetime import datetime, timedelta
from rest_framework.views import APIView

from habits.models.dormir_model import Dormir
from habits.models.despertar_model import Despertar
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto


class ExportarDormirExcelView(APIView):
    def get(self, request):
        usuario = request.query_params.get('usuario')
        proyecto_id = request.query_params.get('proyecto')

        queryset = Dormir.objects.all().order_by('fecha')

        if usuario:
            queryset = queryset.filter(
                usuario__datospersonalesusuario__nombres_apellidos__icontains=usuario
            )

        if proyecto_id:
            queryset = queryset.filter(
                usuario__usuarioproyecto__proyecto__id=proyecto_id
            ).distinct()

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sueño"

        headers = [
            'Fecha', 'Nombre completo', 'Teléfono', 'Hora dormir', 'Hora despertar',
            'Total horas', 'Total minutos', 'Estado', 'Proyecto'
        ]
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for dormir in queryset:
            usuario_id = dormir.usuario.id
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=usuario_id).first()
            nombre = datos_personales.nombres_apellidos if datos_personales else 'N/A'
            telefono = datos_personales.telefono if datos_personales else 'N/A'

            proyecto_nombre = 'N/A'
            usuario_proyecto = UsuarioProyecto.objects.filter(usuario_id=usuario_id).select_related('proyecto').first()
            if usuario_proyecto and usuario_proyecto.proyecto:
                proyecto_nombre = usuario_proyecto.proyecto.nombre

            hora_dormir_str = dormir.hora.strftime("%H:%M:%S")

            total_horas = 0
            total_minutos = 0
            hora_despertar_str = ''
            estado = ''

            registros_despertar = Despertar.objects.filter(
                usuario_id=usuario_id,
                fecha__gte=dormir.fecha
            ).order_by('fecha', 'hora')

            for despertar in registros_despertar:
                hora_dormir = datetime.combine(dormir.fecha, dormir.hora)
                hora_despertar = datetime.combine(despertar.fecha, despertar.hora)

                if hora_despertar < hora_dormir:
                    hora_despertar += timedelta(days=1)

                tiempo_dormido = (hora_despertar - hora_dormir).total_seconds()
                horas = int(tiempo_dormido // 3600)
                minutos = int((tiempo_dormido % 3600) // 60)

                total_horas += horas
                total_minutos += minutos

                if total_minutos >= 60:
                    total_horas += total_minutos // 60
                    total_minutos = total_minutos % 60

                hora_despertar_str = despertar.hora.strftime("%H:%M:%S")
                estado = despertar.estado
                break

            ws.append([
                dormir.fecha.strftime('%Y-%m-%d'),
                nombre,
                telefono,
                hora_dormir_str,
                hora_despertar_str,
                total_horas,
                total_minutos,
                estado,
                proyecto_nombre
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=dormir.xlsx'
        wb.save(response)
        return response
