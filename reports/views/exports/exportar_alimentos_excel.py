import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from rest_framework.views import APIView

from habits.models.alimentacion_model import Alimentacion
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto 

class ExportarAlimentacionExcelView(APIView):
    def get(self, request):
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        queryset = Alimentacion.objects.all().order_by('fecha')

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
        ws.title = "Alimentación"

        headers = [
            'Fecha',
            'Nombre completo',
            'Desayuno', 'Hora desayuno',
            'Almuerzo', 'Hora almuerzo',
            'Cena', 'Hora cena',
            'Proyecto'
        ]
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for registro in queryset:
            datos_personales = DatosPersonalesUsuario.objects.filter(usuario_id=registro.usuario_id).first()
            nombre = datos_personales.nombres_apellidos if datos_personales else "N/A"

            proyecto_nombre = "N/A"
            usuario_proyecto = UsuarioProyecto.objects.filter(usuario_id=registro.usuario_id).select_related('proyecto').first()
            if usuario_proyecto and usuario_proyecto.proyecto:
                proyecto_nombre = usuario_proyecto.proyecto.nombre

            ws.append([
                registro.fecha.strftime('%Y-%m-%d') if registro.fecha else '',
                nombre,
                registro.desayuno or '',
                registro.desayuno_hora.strftime('%H:%M') if registro.desayuno_hora else '',
                registro.almuerzo or '',
                registro.almuerzo_hora.strftime('%H:%M') if registro.almuerzo_hora else '',
                registro.cena or '',
                registro.cena_hora.strftime('%H:%M') if registro.cena_hora else '',
                proyecto_nombre
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=alimentacion.xlsx'
        wb.save(response)
        return response
