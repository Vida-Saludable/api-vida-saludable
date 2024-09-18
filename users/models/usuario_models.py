from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from users.auth.core.autenticacion_usuario import UsuarioManager
from .role_model import Role




class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(max_length=50, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambia esto para evitar el conflicto
        blank=True,
        help_text='Los grupos a los que pertenece este usuario.',
        verbose_name='grupos'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permisos_set',  # Cambia esto para evitar el conflicto
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario'
    )

    def __str__(self):
        return self.correo








