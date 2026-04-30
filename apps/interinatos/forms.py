from django import forms

from .models import Interinato


class InterinatoForm(forms.ModelForm):
    class Meta:
        model = Interinato
        fields = [
            'cargo_interino',
            'dependencia',
            'numero_resolucion',
            'fecha_resolucion',
            'fecha_inicio',
            'fecha_fin',
            'archivo_resolucion',
            'observacion',
        ]
        widgets = {
            'cargo_interino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.: Jefe interino de Departamento'}),
            'dependencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dependencia o área donde ejercerá el interinato'}),
            'numero_resolucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej.: Resolución N° 123/2026'}),
            'fecha_resolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'archivo_resolucion': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf,.pdf'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observación opcional'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['cargo_interino', 'numero_resolucion', 'fecha_inicio', 'fecha_fin', 'archivo_resolucion']:
            self.fields[name].required = True
        if self.instance and self.instance.pk and self.instance.archivo_resolucion:
            self.fields['archivo_resolucion'].required = False

    def clean_archivo_resolucion(self):
        archivo = self.cleaned_data.get('archivo_resolucion')
        if not archivo:
            return archivo
        content_type = getattr(archivo, 'content_type', '')
        name = getattr(archivo, 'name', '').lower()
        if content_type and content_type != 'application/pdf' and not name.endswith('.pdf'):
            raise forms.ValidationError('El archivo de resolución debe estar en formato PDF.')
        if not name.endswith('.pdf'):
            raise forms.ValidationError('El archivo de resolución debe tener extensión .pdf.')
        return archivo

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if inicio and fin and fin < inicio:
            self.add_error('fecha_fin', 'La fecha de fin no puede ser anterior a la fecha de inicio.')
        return cleaned
