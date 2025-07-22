from django.test import TestCase
from datetime import date
from ...models.usuario_models import Usuario
from ...models.datos_personales_usuario_model import DatosPersonalesUsuario

class DatosPersonalesUsuarioTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.usuario = Usuario.objects.create_user(
            correo='test@example.com',
            nombre='Usuario Test',
            password='testpass123'
        )
        
        # Datos completos
        self.datos_completos = {
            'nombres_apellidos': 'Juan Pérez',
            'sexo': 'Masculino',
            'edad': 30,
            'estado_civil': 'Soltero',
            'fecha_nacimiento': date(1993, 5, 15),
            'telefono': '68756940',
            'ocupacion': 'Ingeniero',
            'procedencia': 'Santa Cruz',
            'religion': 'Católico',
            'fecha': date.today(),
            'usuario': self.usuario
        }

    def test_creacion_datos_personales(self):
        """Prueba la creación básica del modelo"""
        datos = DatosPersonalesUsuario.objects.create(**self.datos_completos)
        
        self.assertEqual(datos.nombres_apellidos, 'Juan Pérez')
        self.assertEqual(datos.usuario.correo, 'test@example.com')
        self.assertEqual(datos.edad, 30)
        self.assertTrue(isinstance(datos, DatosPersonalesUsuario))

    def test_campos_opcionales(self):
        """Verifica que los campos pueden ser nulos o vacíos"""
        datos = DatosPersonalesUsuario.objects.create(
            usuario=self.usuario,
            nombres_apellidos=None,
            telefono=''
        )
        
        self.assertIsNone(datos.nombres_apellidos)
        self.assertEqual(datos.telefono, '')

    def test_relacion_usuario(self):
        """Prueba la relación con el modelo Usuario"""
        datos = DatosPersonalesUsuario.objects.create(
            nombres_apellidos='Ana García',
            usuario=self.usuario
        )
        
        self.assertEqual(datos.usuario.id, self.usuario.id)
        self.assertEqual(str(datos), f"Ana García - test@example.com")

    def test_fechas_validas(self):
        """Verifica el manejo correcto de campos de fecha"""
        test_date = date(1990, 1, 1)
        datos = DatosPersonalesUsuario.objects.create(
            usuario=self.usuario,
            fecha_nacimiento=test_date,
            fecha=date.today()
        )
        
        self.assertEqual(datos.fecha_nacimiento, test_date)
        self.assertEqual(datos.fecha, date.today())

    def test_str_representation(self):
        """Prueba la representación en string del modelo"""
        datos = DatosPersonalesUsuario.objects.create(
            nombres_apellidos='María López',
            usuario=self.usuario
        )
        
        self.assertEqual(str(datos), "María López - test@example.com")