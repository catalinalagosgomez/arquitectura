# Generated by Django 5.1.3 on 2024-11-14 08:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_mirador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residente',
            name='fecha_ingreso',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
