from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Sum
from habits.models.alimentacion_model import Alimentacion

class ReportePorcentajeAlimentacionView(APIView):
    def get(self, request, usuario_id):
        # Filtra los registros de alimentación para el usuario específico
        alimentos = Alimentacion.objects.filter(usuario_id=usuario_id)

        # Calcula el total de comidas (desayuno, almuerzo, cena) y el total de comidas saludables
        total_alimentos = alimentos.aggregate(
            total=Sum(F('desayuno') + F('almuerzo') + F('cena'))
        )['total'] or 0

        si_saludables = alimentos.aggregate(
            total_saludables=Sum(F('desayuno_saludable') + F('almuerzo_saludable') + F('cena_saludable'))
        )['total_saludables'] or 0

        # Calcula el porcentaje de comidas saludables y no saludables
        si_saludables_pct = round((si_saludables * 100.0 / total_alimentos), 2) if total_alimentos > 0 else 0
        no_saludables_pct = round(100.0 - si_saludables_pct, 2) if total_alimentos > 0 else 0

        # Estructura el resultado
        resultado = {
            "success": True,
            "message": "Estadísticas de alimentación obtenidas correctamente.",
            "data": {
                "total_alimentos": total_alimentos,
                "si_saludables": si_saludables_pct,
                "no_saludables": no_saludables_pct,
            }
        }

        return Response(resultado, status=status.HTTP_200_OK)

class ReportePorcentajeAlimentacionTipoView(APIView):
    def get(self, request, usuario_id, tipo_alimento):
        # Define los campos de alimentos y saludables de acuerdo al tipo_alimento
        tipo_comida = {
            'desayuno': ('desayuno', 'desayuno_saludable'),
            'almuerzo': ('almuerzo', 'almuerzo_saludable'),
            'cena': ('cena', 'cena_saludable')
        }
        
        if tipo_alimento not in tipo_comida:
            return Response(
                {"success": False, "message": "Tipo de alimento no válido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        alimento_field, saludable_field = tipo_comida[tipo_alimento]

        # Filtra los registros de alimentación para el usuario específico
        alimentos = Alimentacion.objects.filter(usuario_id=usuario_id)

        # Calcula el total de comidas y el total de comidas saludables para el tipo de alimento
        total_alimentos = alimentos.aggregate(
            total=Sum(F(alimento_field))
        )['total'] or 0

        si_saludables = alimentos.aggregate(
            total_saludables=Sum(F(saludable_field))
        )['total_saludables'] or 0

        # Calcula el porcentaje de comidas saludables y no saludables
        si_saludables_pct = round((si_saludables * 100.0 / total_alimentos), 2) if total_alimentos > 0 else 0
        no_saludables_pct = round(100.0 - si_saludables_pct, 2) if total_alimentos > 0 else 0

        # Estructura el resultado
        resultado = {
            "success": True,
            "message": f"Estadísticas de alimentación para {tipo_alimento} obtenidas correctamente.",
            "data": {
                "total_alimentos": total_alimentos,
                "si_saludables": si_saludables_pct,
                "no_saludables": no_saludables_pct,
            }
        }

        return Response(resultado, status=status.HTTP_200_OK)