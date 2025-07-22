from django.test import TestCase
from datetime import date, time
from users.models.usuario_models import Usuario
from ...models.agua_model import Agua

class AguaModelTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.usuario = Usuario.objects.create_user(
            correo='usuario@test.com',
            nombre='Usuario Test',
            password='testpass123'
        )
        
        # Datos de prueba
        self.datos_validos = {
            'fecha': date.today(),
            'hora': time(10, 30),
            'cantidad': 500,  # ml
            'usuario': self.usuario
        }

    def test_creacion_registro_agua(self):
        """Prueba la creación básica de un registro de agua"""
        registro = Agua.objects.create(**self.datos_validos)
        
        self.assertEqual(registro.cantidad, 500)
        self.assertEqual(registro.fecha, date.today())
        self.assertEqual(registro.hora, time(10, 30))
        self.assertEqual(str(registro), f"500ml ({date.today()} {time(10, 30)})")

    def test_campos_obligatorios(self):
        """Valida que todos los campos son requeridos"""
        campos_requeridos = ['fecha', 'hora', 'cantidad', 'usuario']
        
        for campo in campos_requeridos:
            datos_incompletos = self.datos_validos.copy()
            datos_incompletos.pop(campo)
            
            with self.assertRaises(Exception):
                Agua.objects.create(**datos_incompletos)

    def test_cantidad_positiva(self):
        """Verifica que la cantidad debe ser un número positivo"""
        with self.assertRaises(Exception):
            Agua.objects.create(
                fecha=date.today(),
                hora=time(12, 0),
                cantidad=-250,  # Valor negativo
                usuario=self.usuario
            )

    def test_relacion_usuario(self):
        """Prueba la relación con el modelo Usuario"""
        registro = Agua.objects.create(**self.datos_validos)
        
        self.assertEqual(registro.usuario.id, self.usuario.id)
        
        # Prueba eliminación en cascada
        self.usuario.delete()
        with self.assertRaises(Agua.DoesNotExist):
            Agua.objects.get(id=registro.id)

    def test_valores_limite(self):
        """Prueba valores límite para la cantidad de agua"""
        casos_limite = [
            {'cantidad': 1},       # Mínimo valor
            {'cantidad': 1000},    # Valor típico
            {'cantidad': 5000}     # Valor alto
        ]
        
        for caso in casos_limite:
            datos = self.datos_validos.copy()
            datos.update(caso)
            
            registro = Agua.objects.create(**datos)
            self.assertIsNotNone(registro)
            self.assertEqual(registro.cantidad, caso['cantidad'])