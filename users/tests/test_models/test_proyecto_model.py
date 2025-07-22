from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from ...models.proyecto_model import Proyecto

class ProyectoModelTestCase(TestCase):
    def setUp(self):
        self.proyecto_data = {
            'nombre': 'Proyecto Alpha',
            'descripcion': 'Proyecto de prueba',
            'fecha_inicio': date.today(),
            'estado': 1
        }

    def test_fechas_validas(self):
        """Prueba que fecha_fin no puede ser anterior a fecha_inicio"""
        proyecto = Proyecto(
            nombre='Proyecto Inválido',
            fecha_inicio=date.today(),
            fecha_fin=date.today() - timedelta(days=1),
            estado=1
        )
        
        with self.assertRaises(ValidationError) as context:
            proyecto.full_clean()
        
        self.assertIn('fecha_fin', str(context.exception))

    def test_estados_validos(self):
        """Prueba que el estado no puede ser negativo"""
        proyecto = Proyecto.objects.create(**self.proyecto_data)
        proyecto.estado = -1
        
        with self.assertRaises(ValidationError) as context:
            proyecto.full_clean()
        
        self.assertIn('estado', str(context.exception))

    # Mantén las otras pruebas que sí funcionaban
    def test_creacion_proyecto(self):
        proyecto = Proyecto.objects.create(**self.proyecto_data)
        self.assertEqual(proyecto.nombre, 'Proyecto Alpha')

    def test_campos_obligatorios(self):
        with self.assertRaises(ValidationError):
            Proyecto().full_clean()

    def test_nombre_unico(self):
        Proyecto.objects.create(**self.proyecto_data)
        with self.assertRaises(Exception):
            Proyecto.objects.create(**self.proyecto_data)

    def test_str_representation(self):
        proyecto = Proyecto.objects.create(**self.proyecto_data)
        self.assertEqual(str(proyecto), 'Proyecto Alpha')

    def test_proyecto_con_fecha_fin(self):
        proyecto = Proyecto.objects.create(
            nombre='Proyecto Beta',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            estado=1
        )
        self.assertIsNotNone(proyecto.fecha_fin)