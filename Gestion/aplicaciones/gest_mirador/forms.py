from django import forms
from .models import Residente, Pago

class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = [
            'nombre',
            'apellido',
            'rut',
            'numero_departamento',
            'tipo_residente',
            'telefono',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_residente': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['residente', 'tipo_pago', 'monto', 'fecha_vencimiento', 'descripcion']
        widgets = {
            'residente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_monto(self):
        monto = self.cleaned_data['monto']
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor a cero.")
        return monto

    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data['fecha_vencimiento']
        if fecha is None:
            raise forms.ValidationError("Debes proporcionar una fecha válida.")
        return fecha