from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, password=None, role=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not nombre:
            raise ValueError('El usuario debe tener un nombre')
        
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, nombre=nombre, role=role, **extra_fields)
        usuario.set_password(password)  
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuario debe tener is_superuser=True.')

        return self.create_user(correo, nombre, password, **extra_fields)

