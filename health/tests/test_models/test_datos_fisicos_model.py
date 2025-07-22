from django.test import TestCase
from datetime import date
from decimal import Decimal
from users.models.usuario_models import Usuario
from ...models.datos_fisicos_models import DatosFisicos

class DatosFisicosModelTestCase(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.usuario = Usuario.objects.create_user(
            correo='paciente@test.com',
            nombre='Paciente Ejemplo',
            password='testpass123'
        )
        
        # Datos de prueba completos (sin IMC ya que se calculará automáticamente)
        self.datos_completos = {
            'usuario': self.usuario,
            'peso': Decimal('70.50'),
            'altura': 170,
            'radio_abdominal': Decimal('85.00'),
            'grasa_corporal': Decimal('22.50'),
            'grasa_visceral': Decimal('10.00'),
            'porcentaje_musculo': Decimal('45.5'),
            'fecha': date.today(),
            'tipo': 'inicial'
        }

    def test_creacion_datos_fisicos_completos(self):
        """Prueba la creación con todos los campos y cálculo automático de IMC"""
        datos = DatosFisicos.objects.create(**self.datos_completos)
        self.assertEqual(datos.imc, Decimal('24.39'))  # Ahora coincidirá exactamente

    def test_calculo_imc_automatico(self):
        """Prueba el cálculo automático del IMC en diferentes escenarios"""
        datos = DatosFisicos.objects.create(
            usuario=self.usuario,
            peso=Decimal('68'),
            altura=165,
            fecha=date.today(),
            tipo='inicial'
        )
        self.assertEqual(datos.imc, Decimal('24.98'))  # 68 / (1.65^2) redondeado
        
        datos_extremos = DatosFisicos.objects.create(
            usuario=self.usuario,
            peso=Decimal('120'),
            altura=150,
            fecha=date.today(),
            tipo='final'
        )
        self.assertEqual(datos_extremos.imc, Decimal('53.33'))

    def test_actualizacion_imc(self):
        """Verifica que el IMC se actualiza al modificar peso o altura"""
        datos = DatosFisicos.objects.create(
            usuario=self.usuario,
            peso=Decimal('70'),
            altura=170,
            fecha=date.today(),
            tipo='inicial'
        )
        self.assertEqual(datos.imc, Decimal('24.22'))
        
        datos.peso = Decimal('75')
        datos.save()
        self.assertEqual(datos.imc, Decimal('25.95'))
        
        datos.altura = 175
        datos.save()
        self.assertEqual(datos.imc, Decimal('24.49'))

    def test_sin_calculo_imc_sin_datos(self):
        """Valida que no se calcule IMC si faltan peso o altura"""
        datos_sin_peso = DatosFisicos.objects.create(
            usuario=self.usuario,
            altura=170,
            fecha=date.today(),
            tipo='inicial'
        )
        self.assertIsNone(datos_sin_peso.imc)
        
        datos_sin_altura = DatosFisicos.objects.create(
            usuario=self.usuario,
            peso=Decimal('70'),
            fecha=date.today(),
            tipo='inicial'
        )
        self.assertIsNone(datos_sin_altura.imc)

    def test_campos_opcionales(self):
        """Verifica que los campos numéricos pueden ser nulos"""
        datos = DatosFisicos.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='final',
            peso=None,
            altura=None
        )
        
        self.assertIsNone(datos.peso)
        self.assertIsNone(datos.altura)

    def test_campos_obligatorios(self):
        """Valida que fecha y tipo son requeridos"""
        with self.assertRaises(Exception):
            DatosFisicos.objects.create(
                usuario=self.usuario,
                tipo='inicial'  # Falta fecha
            )
            
        with self.assertRaises(Exception):
            DatosFisicos.objects.create(
                usuario=self.usuario,
                fecha=date.today()  # Falta tipo
            )

    def test_decimales_validos(self):
        """Prueba el manejo correcto de valores decimales"""
        datos = DatosFisicos.objects.create(
            usuario=self.usuario,
            peso=Decimal('85.25'),
            grasa_corporal=Decimal('30.75'),
            fecha=date.today(),
            tipo='final'
        )
        
        self.assertEqual(datos.peso, Decimal('85.25'))
        self.assertEqual(datos.grasa_corporal, Decimal('30.75'))

    def test_relacion_usuario(self):
        """Verifica la integridad de la relación con Usuario"""
        datos = DatosFisicos.objects.create(
            usuario=self.usuario,
            fecha=date.today(),
            tipo='inicial'
        )
        
        self.assertEqual(datos.usuario.id, self.usuario.id)
        
        # Prueba eliminación en cascada
        self.usuario.delete()
        with self.assertRaises(DatosFisicos.DoesNotExist):
            DatosFisicos.objects.get(id=datos.id)

    def test_tipos_permitidos(self):
        """Valida el campo tipo con valores permitidos"""
        for tipo_valido in ['inicial', 'final']:
            datos = DatosFisicos.objects.create(
                usuario=self.usuario,
                fecha=date.today(),
                tipo=tipo_valido
            )
            self.assertEqual(datos.tipo, tipo_valido)