import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from rest_framework.views import APIView

from habits.models.sol_model import Sol
from users.models.datos_personales_usuario_model import DatosPersonalesUsuario
from users.models.usuario_proyecto_model import UsuarioProyecto


class ExportarSolExcelView(APIView):
    def get(self, request):
        usuario = request.query_params.get('usuario', None)
        proyecto_id = request.query_params.get('proyecto', None)

        queryset = Sol.objects.all().order_by('fecha')

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
        ws.title = "Sol"

        headers = ['Fecha', 'Nombre completo', 'Tiempo (min)', 'Proyecto']
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
                registro.tiempo if registro.tiempo is not None else '',
                proyecto_nombre
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=sol.xlsx'
        wb.save(response)
        return response
