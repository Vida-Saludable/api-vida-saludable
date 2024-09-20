# Generated by Django 5.0.7 on 2024-09-20 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosCorporales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('imc', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('presion_sistolica', models.IntegerField(blank=True, null=True)),
                ('presion_diastolica', models.IntegerField(blank=True, null=True)),
                ('radio_abdominal', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('grasa_corporal', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('grasa_visceral', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('frecuencia_cardiaca', models.IntegerField(blank=True, null=True)),
                ('frecuencia_respiratoria', models.IntegerField(blank=True, null=True)),
                ('colesterol_total', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('colesterol_hdl', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('colesterol_ldl', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('trigliceridos', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('glucosa', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('temperatura', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('saturacion_oxigeno', models.IntegerField(blank=True, null=True)),
                ('porcentaje_musculo', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('glicemia_basal', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('frecuencia_cardiaca_en_reposo', models.IntegerField(blank=True, null=True)),
                ('frecuencia_cardiaca_despues_de_45_segundos', models.IntegerField(blank=True, null=True)),
                ('frecuencia_cardiaca_1_minuto_despues', models.IntegerField(blank=True, null=True)),
                ('resultado_test_rufier', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(max_length=20)),
            ],
        ),
    ]
