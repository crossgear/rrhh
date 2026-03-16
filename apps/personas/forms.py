"""
Formularios para la app personas
"""
from django import forms
from django.core.validators import RegexValidator
from .models import Persona


class PersonaForm(forms.ModelForm):
    """
    Formulario para crear/editar personas.
    """
    class Meta:
        model = Persona
        fields = [
            'CI_NUMERO',
            'NOMBRES',
            'APELLIDOS',
            'FECHA_NACIMIENTO',
            'ESTADO_CIVIL',
            'TELEFONO',
            'EMAIL',
            'ACTIVO'
        ]
        widgets = {
            'CI_NUMERO': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1234567',
                'maxlength': 20
            }),
            'NOMBRES': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres completos'
            }),
            'APELLIDOS': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos completos'
            }),
            'FECHA_NACIMIENTO': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ESTADO_CIVIL': forms.Select(attrs={'class': 'form-select'}),
            'TELEFONO': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0981123456'
            }),
            'EMAIL': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'ACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_CI_NUMERO(self):
        ci = self.cleaned_data.get('CI_NUMERO')
        if not ci:
            return ci
        # Validar que solo contenga números y guiones
        import re
        if not re.match(r'^[0-9\-]+$', ci):
            raise forms.ValidationError('La cédula solo puede contener números y guiones.')
        return ci.upper()

    def clean_email(self):
        email = self.cleaned_data.get('EMAIL')
        if email:
            # Django valida el formato email automáticamente
            pass
        return email
