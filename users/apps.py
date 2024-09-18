from django.apps import AppConfig


<<<<<<<< HEAD:reports/apps.py
class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
========
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
>>>>>>>> af0a3a661551e346058a3b3d83079c2aac70a65e:users/apps.py
