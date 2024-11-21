

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gest_mirador', '0002_alter_residente_fecha_ingreso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('GC', 'Gasto Común'), ('GE', 'Gasto Extraordinario'), ('OS', 'Otro Servicio')], max_length=2)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_vencimiento', models.DateField()),
                ('fecha_pago', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PAGADO', 'Pagado'), ('ATRASADO', 'Atrasado')], default='PENDIENTE', max_length=10)),
                ('comprobante', models.FileField(blank=True, null=True, upload_to='comprobantes/')),
                ('descripcion', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest_mirador.residente')),
            ],
        ),
        migrations.CreateModel(
            name='Recordatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('enviado', models.BooleanField(default=False)),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gest_mirador.pago')),
            ],
        ),
    ]
