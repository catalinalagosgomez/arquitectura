from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Residente, Pago
from .forms import ResidenteForm, PagoForm

from .singleton import GestorResidentes
from .singleton import GestorPagos
from .forms import PagoForm

def home(request):
    return render(request,"menu_gest.html")

def gestion_pagos(request):
    return render(request,"gestion_pagos.html")

def menu_resid(request):
    return render(request, 'gest_mirador/menu_resid.html')

def agregar_residente(request):
    gestor = GestorResidentes()
    if request.method == 'POST':
        form = ResidenteForm(request.POST)
        if form.is_valid():
            gestor.crear_residente(form)
            messages.success(request, 'Residente agregado exitosamente.')
            return redirect('listar_residentes')
    else:
        form = ResidenteForm()
    
    return render(request, 'gest_mirador/agregar_residente.html', {'form': form})


class ResidentUpdateView(UpdateView):
    model = Residente
    form_class = ResidenteForm
    template_name = 'residents/resident_form.html'
    success_url = reverse_lazy('resident_list')

    def form_valid(self, form):
        messages.success(self.request, 'Residente actualizado exitosamente.')
        return super().form_valid(form)

# Vista para eliminar residente
class ResidentDeleteView(DeleteView):
    model = Residente
    template_name = 'residents/resident_confirm_delete.html'
    success_url = reverse_lazy('resident_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Residente eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


def gestion_residentes(request):
    return render(request,"gestion_residentes.html")

def listar_residentes(request):
    gestor = GestorResidentes()
    residentes = gestor.obtener_residentes()
    return render(request, 'gest_mirador/listar_residentes.html', {'residentes': residentes})

def eliminar_residente(request, id):
    gestor = GestorResidentes()
    if gestor.eliminar_residente(id):
        messages.success(request, 'Residente eliminado exitosamente.')
    return redirect('listar_residentes')

def editar_residente(request, id):
    gestor = GestorResidentes()
    residente = gestor.obtener_residente(id)
    if request.method == 'POST':
        form = ResidenteForm(request.POST, instance=residente)
        if gestor.actualizar_residente(id, form):
            messages.success(request, 'Residente actualizado exitosamente.')
            return redirect('listar_residentes')
    else:
        form = ResidenteForm(instance=residente)
    return render(request, 'gest_mirador/editar_residente.html', {'form': form, 'residente': residente})

def registrar_pago(request):
    gestorpago = GestorPagos()
    if request.method == 'POST':
        form = PagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save()  
            messages.success(request, 'Pago registrado exitosamente.')
            return redirect('listar_pagos')  
        else:
             messages.error(request, 'Error al registrar el pago. Por favor, revisa los datos.')
             print(form.errors)  

    else:
        form = PagoForm()
    
    return render(request, 'gest_mirador/registrar_pago.html', {'form': form})

def listar_pagos(request):
    gestor = GestorPagos()
    pagos_pendientes = gestor.obtener_pagos_pendientes()
    return render(request, 'gest_mirador/listar_pagos.html', {'pagos': pagos_pendientes})

def procesar_pago(request, pago_id):
    gestor = GestorPagos()
    if request.method == 'POST':
        try:
            pago = gestor.procesar_pago(
                pago_id,
                comprobante=request.FILES.get('comprobante')#guarda los comprobantes en un FILE o carpeta 
            )
            messages.success(request, 'Pago procesado exitosamente.')
            return redirect('listar_pagos')
        except Exception as e:
            messages.error(request, str(e))
    return redirect('listar_pagos')

def recibo_pago(request, id):
    gestor = GestorPagos()
    try:
        pago = get_object_or_404(Pago, id=id)
        recibo_data = gestor.generar_recibo(id)
        
        context = {
            'recibo': {
                'numero_recibo': recibo_data['numero_recibo'],
                'fecha': pago.fecha_pago,
                'residente': f"{pago.residente.nombre} {pago.residente.apellido}",
                'monto': pago.monto,
                'tipo_pago': pago.get_tipo_pago_display(),
                'descripcion': pago.descripcion
            }
        }
        return render(request, 'gest_mirador/recibo_pago.html', context)
    except Exception as e:
        messages.error(request, f"Error al generar recibo: {str(e)}")
        return redirect('listar_pagos')

def menu_pagos(request):
    return render(request, 'gest_mirador/menu_pagos.html')

def menu_gest(request):
       return render(request, 'gest_mirador/menu_gest.html')
