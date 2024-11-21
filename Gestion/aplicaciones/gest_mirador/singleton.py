from .models import Residente
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from .models import Pago, Recordatorio, Residente
from django.core.mail import send_mail
from django.conf import settings


class GestorResidentes:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Evitar reinicialización del singleton
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def obtener_residentes(self):
        return Residente.objects.filter(activo=True)

    def obtener_residente(self, id):
        return get_object_or_404(Residente, id=id)

    def crear_residente(self, form):
        try:
            return form.save()
        except ValidationError as e:
            raise ValidationError(f"Error al crear residente: {str(e)}")

    def actualizar_residente(self, id, form):
        try:
            if form.is_valid():
                return form.save()
            return None
        except ValidationError as e:
            raise ValidationError(f"Error al actualizar residente: {str(e)}")

    def eliminar_residente(self, id):
        try:
            residente = self.obtener_residente(id)
            residente.delete()
            return True
        except Exception as e:
            raise Exception(f"Error al eliminar residente: {str(e)}")

def test_singleton():
    gestor1 = GestorResidentes()
    gestor2 = GestorResidentes()
    print(f"¿Son el mismo objeto?: {gestor1 is gestor2}")  


class GestorPagos:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    def registrar_pago(self, residente_id, tipo_pago, monto, fecha_vencimiento, descripcion=""):
        try:
            residente = Residente.objects.get(id=residente_id)
            pago = Pago.objects.create(
                residente=residente,
                tipo_pago=tipo_pago,
                monto=monto,
                fecha_vencimiento=fecha_vencimiento,
                descripcion=descripcion
            )
            return pago
        except Exception as e:
            raise Exception(f"Error al registrar pago: {str(e)}")

    def procesar_pago(self, pago_id, fecha_pago=None, comprobante=None):
        try:
            pago = Pago.objects.get(id=pago_id)
            pago.estado = 'PAGADO'
            pago.fecha_pago = fecha_pago or timezone.now().date()
            if comprobante:
                pago.comprobante = comprobante
            pago.save()
            return pago
        except Exception as e:
            raise Exception(f"Error al procesar pago: {str(e)}")

    def generar_recibo(self, pago_id):
        try:
            pago = Pago.objects.get(id=pago_id)
            # genera pdf
            recibo_data = {
                'numero_recibo': f"REC-{pago.id}",
                'fecha': pago.fecha_pago,
                'residente': f"{pago.residente.nombre} {pago.residente.apellido}",
                'monto': pago.monto,
                'tipo_pago': pago.get_tipo_pago_display(),
                'descripcion': pago.descripcion
            }
            return recibo_data
        except Exception as e:
            raise Exception(f"Error al generar recibo: {str(e)}")

    def enviar_recordatorio(self, pago_id):
        try:
            pago = Pago.objects.get(id=pago_id)
            if pago.estado != 'PAGADO':
                recordatorio = Recordatorio.objects.create(pago=pago)
                # Enviar email
                send_mail(
                    'Recordatorio de Pago',
                    f'Estimado {pago.residente.nombre}, tiene un pago pendiente por {pago.monto}',
                    settings.EMAIL_HOST_USER,
                    [pago.residente.email],
                    fail_silently=False,
                )
                recordatorio.enviado = True
                recordatorio.save()
                return True
            return False
        except Exception as e:
            raise Exception(f"Error al enviar recordatorio: {str(e)}")

    def verificar_morosidad(self):
        try:
            fecha_actual = timezone.now().date()
            pagos_atrasados = Pago.objects.filter(
                estado='PENDIENTE',
                fecha_vencimiento__lt=fecha_actual
            )
            for pago in pagos_atrasados:
                pago.estado = 'ATRASADO'
                pago.save()
            return pagos_atrasados
        except Exception as e:
            raise Exception(f"Error al verificar morosidad: {str(e)}")

    def obtener_pagos_pendientes(self, residente_id=None):
        try:
            if residente_id:
                return Pago.objects.filter(residente_id=residente_id, estado='PENDIENTE')
            return Pago.objects.filter(estado='PENDIENTE')
        except Exception as e:
            raise Exception(f"Error al obtener pagos pendientes: {str(e)}")

    def obtener_historial_pagos(self, residente_id):
        try:
            return Pago.objects.filter(residente_id=residente_id).order_by('-fecha_vencimiento')
        except Exception as e:
            raise Exception(f"Error al obtener historial de pagos: {str(e)}")