from django.test import TestCase
from django.contrib.auth.hashers import check_password
from datetime import date
from ...models.role_model import Role
from ...models.usuario_models import Usuario
from ...models.proyecto_model import Proyecto
from ...models.usuario_proyecto_model import UsuarioProyecto

class UsuarioModelTestCase(TestCase):
    def setUp(self):
        # Datos básicos para crear un usuario
        self.usuario_data = {
            'correo': 'test@example.com',
            'nombre': 'Usuario de Prueba',
            'password': 'testpass123'
        }
        
        # Crear datos para pruebas de roles y proyectos
        self.rol_desarrollador = Role.objects.create(name="Desarrollador")
        self.rol_lider = Role.objects.create(name="Líder de Proyecto")
        
        # Proyectos con fecha_inicio requerida
        self.proyecto_alpha = Proyecto.objects.create(
            nombre="Proyecto Alpha",
            fecha_inicio=date.today(),  # Añade la fecha requerida
            estado=0
        )
        self.proyecto_beta = Proyecto.objects.create(
            nombre="Proyecto Beta",
            fecha_inicio=date.today(),
            estado=1
        )

    # PRUEBAS BÁSICAS DE USUARIO
    def test_creacion_usuario_normal(self):
        """Prueba que un usuario se puede crear correctamente"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        
        self.assertEqual(usuario.correo, self.usuario_data['correo'])
        self.assertEqual(usuario.nombre, self.usuario_data['nombre'])
        self.assertTrue(check_password(self.usuario_data['password'], usuario.password))
        self.assertTrue(usuario.is_active)
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.is_superuser)

    def test_campos_obligatorios(self):
        """Verifica que 'correo' y 'nombre' sean requeridos"""
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(correo=None, nombre="Sin Email", password="test123")
        
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(correo="test@example.com", nombre=None, password="test123")

    def test_creacion_superusuario(self):
        """Prueba la creación de un superusuario"""
        superuser = Usuario.objects.create_superuser(
            correo='admin@example.com',
            nombre='Admin',
            password='admin123'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_str_representation(self):
        """Prueba el método __str__"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertEqual(str(usuario), self.usuario_data['correo'])

    def test_get_full_name(self):
        """Prueba el método get_full_name()"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertEqual(usuario.get_full_name(), self.usuario_data['nombre'])

    # PRUEBAS DE ASIGNACIÓN DE ROLES
    def test_asignacion_rol_a_usuario(self):
        """Prueba que un usuario puede tener un rol asignado"""
        usuario = Usuario.objects.create_user(
            **self.usuario_data,
            role=self.rol_desarrollador
        )
        
        self.assertEqual(usuario.role.name, "Desarrollador")
        self.assertTrue(isinstance(usuario.role, Role))
        self.assertEqual(usuario.role.id, self.rol_desarrollador.id)

    def test_usuario_sin_rol(self):
        """Prueba que el rol no es obligatorio"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertIsNone(usuario.role)

    def test_cambio_rol_usuario(self):
        """Prueba que se puede cambiar el rol de un usuario"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        usuario.role = self.rol_lider
        usuario.save()
        
        usuario.refresh_from_db()
        self.assertEqual(usuario.role.name, "Líder de Proyecto")

    # PRUEBAS DE ASIGNACIÓN DE PROYECTOS (Usando UsuarioProyecto)
    def test_asignacion_proyecto_a_usuario(self):
        """Prueba la asignación básica de un proyecto a un usuario"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        relacion = UsuarioProyecto.objects.create(
            usuario=usuario,
            proyecto=self.proyecto_alpha
        )
        
        self.assertEqual(relacion.usuario.correo, 'test@example.com')
        self.assertEqual(relacion.proyecto.nombre, 'Proyecto Alpha')
        self.assertEqual(str(relacion), 'test@example.com - Proyecto Alpha')

    def test_asignacion_multiple_proyectos(self):
        """Prueba que un usuario puede estar en múltiples proyectos"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        UsuarioProyecto.objects.create(usuario=usuario, proyecto=self.proyecto_alpha)
        UsuarioProyecto.objects.create(usuario=usuario, proyecto=self.proyecto_beta)
        
        proyectos_usuario = Proyecto.objects.filter(usuarioproyecto__usuario=usuario)
        self.assertEqual(proyectos_usuario.count(), 2)
        self.assertIn(self.proyecto_alpha, proyectos_usuario)
        self.assertIn(self.proyecto_beta, proyectos_usuario)

    def test_usuario_unico_por_proyecto(self):
        """Prueba que no se puede asignar el mismo usuario dos veces al mismo proyecto"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        UsuarioProyecto.objects.create(usuario=usuario, proyecto=self.proyecto_alpha)
        
        with self.assertRaises(Exception):  # Por la restricción unique_together
            UsuarioProyecto.objects.create(usuario=usuario, proyecto=self.proyecto_alpha)