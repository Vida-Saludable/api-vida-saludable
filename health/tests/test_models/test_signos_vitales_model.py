from django.test import TestCase
from datetime import date
from decimal import Decimal
from users.models.usuario_models import Usuario
from ...models.signos_vitales_models import SignosVitales

class SignosVitalesModelTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            correo='paciente@test.com',
            nombre='Paciente Ejemplo',
            password='testpass123'
        )
        
        self.datos_completos = {
            'usuario': self.usuario,
            'presion_sistolica': 120,
            'presion_diastolica': 80,
            'frecuencia_cardiaca': 75,
            'frecuencia_respiratoria': 16,
            'temperatura': Decimal('36.5'),
            'saturacion_oxigeno': 98,
            'fecha': date.today(),
            'tipo': 'inicial'
        }

    def test_creacion_signos_vitales_completos(self):
        """Prueba la creación con todos los campos"""
        signos = SignosVitales.objects.create(**self.datos_completos)
        
        self.assertEqual(signos.presion_sistolica, 120)
        self.assertEqual(signos.presion_diastolica, 80)
        self.assertEqual(signos.temperatura, Decimal('36.5'))
        self.assertEqual(str(signos), "Signos Vitales de paciente@test.com (inicial)")

    def test_campos_opcionales(self):
        """Verifica que los campos de signos vitales pueden ser nulos"""
        signos = SignosVitales.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='inicial',
            presion_sistolica=None,
            temperatura=None
        )
        
        self.assertIsNone(signos.presion_sistolica)
        self.assertIsNone(signos.temperatura)

    def test_campos_obligatorios(self):
        """Valida que fecha y tipo son requeridos"""
        with self.assertRaises(Exception):
            SignosVitales.objects.create(
                usuario=self.usuario,
                tipo='inicial'  # Falta fecha
            )
            
        with self.assertRaises(Exception):
            SignosVitales.objects.create(
                usuario=self.usuario,
                fecha=date.today()  # Falta tipo
            )

    def test_temperatura_decimal(self):
        """Prueba el manejo correcto de valores decimales en temperatura"""
        signos = SignosVitales.objects.create(
            usuario=self.usuario,
            temperatura=Decimal('37.2'),
            fecha=date.today(),
            tipo='final'
        )
        
        self.assertEqual(signos.temperatura, Decimal('37.2'))

    def test_relacion_usuario(self):
        """Verifica la integridad de la relación con Usuario"""
        signos = SignosVitales.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='inicial'
        )
        
        self.assertEqual(signos.usuario.id, self.usuario.id)
        
        # Prueba eliminación en cascada
        self.usuario.delete()
        with self.assertRaises(SignosVitales.DoesNotExist):
            SignosVitales.objects.get(id=signos.id)

    def test_tipos_permitidos(self):
        """Valida el campo tipo con valores permitidos"""
        for tipo_valido in ['inicial', 'final']:
            signos = SignosVitales.objects.create(
                usuario=self.usuario,
                fecha=date.today(),
                tipo=tipo_valido
            )
            self.assertEqual(signos.tipo, tipo_valido)