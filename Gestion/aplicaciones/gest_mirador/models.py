from django.db import models
from django.utils import timezone


class Residente(models.Model):
    TIPO_RESIDENCIA = [
        ('P', 'Propietario'),
        ('A', 'Arrendatario'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    
    
    
    tipo_residente = models.CharField(
        max_length=4,
        choices=TIPO_RESIDENCIA,
        default='PROP'
    )
    numero_departamento = models.CharField(max_length=10)
    fecha_ingreso = models.DateField(default=timezone.now)
    

    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Residente'
        verbose_name_plural = 'Residentes'

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Depto: {self.numero_departamento}"


class Pago(models.Model):
    TIPO_PAGO_CHOICES = [
        ('GC', 'Gasto Común'),
        ('GE', 'Gasto Extraordinario'),
        ('OS', 'Otro Servicio')
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ATRASADO', 'Atrasado'),
    ]

    residente = models.ForeignKey('Residente', on_delete=models.CASCADE)
    tipo_pago = models.CharField(max_length=2, choices=TIPO_PAGO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pago {self.tipo_pago} - {self.residente.nombre} {self.residente.apellido}"
    

    def actualizar_estado(self):
        if self.fecha_pago:
            self.estado = 'PAGADO'
        elif self.fecha_vencimiento < timezone.now().date():
            self.estado = 'ATRASADO'
        else:
            self.estado = 'PENDIENTE'
        self.save()

    def procesar_pago(self, comprobante=None):
        if comprobante:
            self.comprobante = comprobante
        self.fecha_pago = timezone.now().date()  
        self.actualizar_estado() 
        self.save()

class Recordatorio(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    enviado = models.BooleanField(default=False)
