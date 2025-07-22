from django.test import TestCase
from datetime import date
from decimal import Decimal
from users.models.usuario_models import Usuario
from ...models.datos_muestras_models import DatosMuestras

class DatosMuestrasModelTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.usuario = Usuario.objects.create_user(
            correo='paciente@test.com',
            nombre='Paciente Ejemplo',
            password='testpass123'
        )
        
        # Datos de muestra completos
        self.datos_completos = {
            'usuario': self.usuario,
            'colesterol_total': Decimal('180.50'),
            'colesterol_hdl': Decimal('45.75'),
            'colesterol_ldl': Decimal('120.25'),
            'trigliceridos': Decimal('150.00'),
            'glucosa': Decimal('95.50'),
            'glicemia_basal': Decimal('92.5'),
            'fecha': date.today(),
            'tipo': 'inicial'
        }

    def test_creacion_datos_completos(self):
        """Prueba la creación con todos los campos"""
        muestra = DatosMuestras.objects.create(**self.datos_completos)
        
        self.assertEqual(muestra.colesterol_total, Decimal('180.50'))
        self.assertEqual(muestra.colesterol_hdl, Decimal('45.75'))
        self.assertEqual(muestra.glicemia_basal, Decimal('92.5'))
        self.assertEqual(str(muestra), "Datos muestras de paciente@test.com (inicial)")

    def test_campos_opcionales(self):
        """Verifica que los campos bioquímicos pueden ser nulos"""
        muestra = DatosMuestras.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='final',
            colesterol_total=None,
            glucosa=None
        )
        
        self.assertIsNone(muestra.colesterol_total)
        self.assertIsNone(muestra.glucosa)

    def test_campos_obligatorios(self):
        """Valida que fecha y tipo son requeridos"""
        with self.assertRaises(Exception):
            DatosMuestras.objects.create(
                usuario=self.usuario,
                tipo='inicial'  # Falta fecha
            )
            
        with self.assertRaises(Exception):
            DatosMuestras.objects.create(
                usuario=self.usuario,
                fecha=date.today()  # Falta tipo
            )

    def test_precision_decimal(self):
        """Prueba la precisión decimal en diferentes campos"""
        muestra = DatosMuestras.objects.create(
            usuario=self.usuario,
            colesterol_total=Decimal('199.99'),
            glicemia_basal=Decimal('99.9'),
            fecha=date.today(),
            tipo='inicial'
        )
        
        self.assertEqual(muestra.colesterol_total, Decimal('199.99'))  # 5 dígitos, 2 decimales
        self.assertEqual(muestra.glicemia_basal, Decimal('99.9'))  # 4 dígitos, 1 decimal

    def test_relacion_usuario(self):
        """Verifica la integridad de la relación con Usuario"""
        muestra = DatosMuestras.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='inicial'
        )
        
        self.assertEqual(muestra.usuario.id, self.usuario.id)
        
        # Prueba eliminación en cascada
        self.usuario.delete()
        with self.assertRaises(DatosMuestras.DoesNotExist):
            DatosMuestras.objects.get(id=muestra.id)

    def test_tipos_permitidos(self):
        """Valida el campo tipo con valores permitidos"""
        for tipo_valido in ['inicial', 'final']:
            muestra = DatosMuestras.objects.create(
                usuario=self.usuario,
                fecha=date.today(),
                tipo=tipo_valido
            )
            self.assertEqual(muestra.tipo, tipo_valido)

    def test_valores_limite(self):
        """Prueba valores límite para indicadores metabólicos"""
        casos_limite = [
            {'colesterol_total': Decimal('50.00')},  # Valor bajo
            {'trigliceridos': Decimal('500.00')},    # Valor alto
            {'glucosa': Decimal('30.00')},           # Hipoglicemia
            {'glicemia_basal': Decimal('300.0')}     # Hiperglicemia
        ]
        
        for caso in casos_limite:
            muestra = DatosMuestras.objects.create(
                usuario=self.usuario,
                fecha=date.today(),
                tipo='inicial',
                **caso
            )
            self.assertIsNotNone(muestra)