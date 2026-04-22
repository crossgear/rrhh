
"""Formularios de ficha personal web."""
from django import forms
from .models import Persona
from apps.laboral.models import DatosLaborales
from apps.academico.models import DatosAcademicos


GRUPO_SANGUINEO_CHOICES = [
    ('', 'Seleccione'),
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
]


class FichaPersonalForm(forms.Form):
    # Datos personales
    CI_NUMERO = forms.CharField(label='C.I. N°', max_length=20)
    NOMBRES = forms.CharField(label='Nombres', max_length=100)
    APELLIDOS = forms.CharField(label='Apellidos', max_length=100)
    FECHA_NACIMIENTO = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    ESTADO_CIVIL = forms.ChoiceField(label='Estado civil', choices=Persona.ESTADO_CIVIL_CHOICES, required=False)
    TELEFONO = forms.CharField(label='Teléfono', max_length=20, required=False)
    CELULAR = forms.CharField(label='Celular', max_length=20, required=True)
    EMAIL = forms.EmailField(label='Correo institucional', required=False)
    DOMICILIO_ACTUAL = forms.CharField(label='Domicilio actual', max_length=200, required=True)
    BARRIO = forms.CharField(label='Barrio', max_length=100, required=True)
    CIUDAD = forms.CharField(label='Ciudad', max_length=100, required=True)
    LATITUD = forms.DecimalField(label='Latitud', required=False, max_digits=10, decimal_places=8, widget=forms.HiddenInput())
    LONGITUD = forms.DecimalField(label='Longitud', required=False, max_digits=11, decimal_places=8, widget=forms.HiddenInput())
    FOTO_CARNET = forms.ImageField(label='Foto carnet', required=True)
    ACTIVO = forms.BooleanField(label='Activo', required=False, initial=True)

    # Datos laborales
    TIPO_VINCULO = forms.ChoiceField(label='Tipo de vínculo', choices=DatosLaborales.TIPO_VINCULO_CHOICES, required=True)
    NUMERO_DECRETO = forms.CharField(label='Decreto N°', max_length=50, required=False)
    FECHA_DECRETO = forms.DateField(label='Fecha decreto', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    NUMERO_RESOLUCION = forms.CharField(label='Resolución N°', max_length=50, required=False)
    FECHA_RESOLUCION = forms.DateField(label='Fecha resolución', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    NUMERO_DGRP = forms.CharField(label='D.G.R.P. N°', max_length=50, required=False)
    FECHA_DGRP = forms.DateField(label='Fecha D.G.R.P.', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    CARGO = forms.CharField(label='Cargo', max_length=150, required=True)
    CATEGORIA = forms.CharField(label='Categoría', max_length=80, required=True)
    SALARIO = forms.DecimalField(label='Salario', required=True, max_digits=12, decimal_places=0, widget=forms.TextInput())
    FECHA_INGRESO = forms.DateField(label='Fecha de ingreso', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    LUGAR_TRABAJO = forms.CharField(label='Lugar de trabajo', max_length=150, required=True)

    # Datos académicos
    NIVEL_PRIMARIO = forms.BooleanField(label='Nivel primario', required=False)
    NIVEL_SECUNDARIO = forms.BooleanField(label='Nivel secundario', required=False)
    NIVEL_UNIVERSITARIO = forms.BooleanField(label='Nivel universitario', required=False)
    BACHILLER = forms.CharField(label='Bachiller', max_length=100, required=False)
    ANIO_BACHILLER = forms.IntegerField(label='Año bachiller', required=False)
    CARRERA = forms.CharField(label='Carrera', max_length=150, required=False)
    ANIO_CARRERA = forms.IntegerField(label='Año carrera', required=False)
    UNIVERSIDAD = forms.CharField(label='Universidad', max_length=150, required=False)
    POSTGRADOS = forms.CharField(label='Postgrados', required=False, widget=forms.Textarea(attrs={'rows': 2}))
    MAESTRIAS = forms.CharField(label='Maestrías', required=False, widget=forms.Textarea(attrs={'rows': 2}))
    DOCTORADOS = forms.CharField(label='Doctorados', required=False, widget=forms.Textarea(attrs={'rows': 2}))
    OTROS_ESTUDIOS = forms.CharField(label='Otros estudios', required=False, widget=forms.Textarea(attrs={'rows': 2}))

    # Historial médico
    ALERGIAS_ENFERMEDADES = forms.CharField(label='Alergias o enfermedades', required=False, widget=forms.Textarea(attrs={'rows': 2}))
    GRUPO_SANGUINEO = forms.ChoiceField(label='Grupo sanguíneo', choices=GRUPO_SANGUINEO_CHOICES, required=True)
    TIENE_SEGURO_MEDICO = forms.BooleanField(label='Seguro médico', required=False)
    SANATORIO = forms.CharField(label='Sanatorio', max_length=150, required=False)
    TELEFONO_SANATORIO = forms.CharField(label='Tel. sanatorio', max_length=20, required=False)

    # Emergencia
    EMERGENCIA_NOMBRE_1 = forms.CharField(label='Contacto emergencia 1', max_length=150, required=True)
    EMERGENCIA_TELEFONO_1 = forms.CharField(label='Teléfono emergencia 1', max_length=20, required=True)
    EMERGENCIA_NOMBRE_2 = forms.CharField(label='Contacto emergencia 2', max_length=150, required=False)
    EMERGENCIA_TELEFONO_2 = forms.CharField(label='Teléfono emergencia 2', max_length=20, required=False)

    # Familiares
    NOMBRE_PADRE = forms.CharField(label='Padre', max_length=150, required=False)
    NOMBRE_MADRE = forms.CharField(label='Madre', max_length=150, required=False)
    NOMBRE_CONYUGE = forms.CharField(label='Cónyuge', max_length=150, required=False)
    HIJO_1_NOMBRE = forms.CharField(label='Hijo/a 1', max_length=150, required=False)
    HIJO_1_FECHA = forms.DateField(label='Fecha Nac. hijo/a 1', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    HIJO_2_NOMBRE = forms.CharField(label='Hijo/a 2', max_length=150, required=False)
    HIJO_2_FECHA = forms.DateField(label='Fecha Nac. hijo/a 2', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    HIJO_3_NOMBRE = forms.CharField(label='Hijo/a 3', max_length=150, required=False)
    HIJO_3_FECHA = forms.DateField(label='Fecha Nac. hijo/a 3', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    HIJO_4_NOMBRE = forms.CharField(label='Hijo/a 4', max_length=150, required=False)
    HIJO_4_FECHA = forms.DateField(label='Fecha Nac. hijo/a 4', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    HIJO_5_NOMBRE = forms.CharField(label='Hijo/a 5', max_length=150, required=False)
    HIJO_5_FECHA = forms.DateField(label='Fecha Nac. hijo/a 5', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    HIJO_6_NOMBRE = forms.CharField(label='Hijo/a 6', max_length=150, required=False)
    HIJO_6_FECHA = forms.DateField(label='Fecha Nac. hijo/a 6', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    # Cierre de ficha
    OBSERVACIONES_FICHA = forms.CharField(label='Observaciones', required=False, widget=forms.Textarea(attrs={'rows': 3}))
    CROQUIS_REFERENCIA = forms.CharField(label='Croquis / referencia del domicilio', required=True, widget=forms.Textarea(attrs={'rows': 3}))
    FIRMA_ACLARACION = forms.CharField(label='Aclaración', max_length=150, required=False)
    FECHA_FIRMA = forms.DateField(label='Fecha', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, persona=None, **kwargs):
        self.persona = persona
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        if persona and not self.is_bound:
            self._load_from_instance(persona)

    def _apply_bootstrap(self):
        required_field_names = {
            'CI_NUMERO', 'NOMBRES', 'APELLIDOS', 'FECHA_NACIMIENTO', 'CELULAR',
            'DOMICILIO_ACTUAL', 'BARRIO', 'CIUDAD', 'FOTO_CARNET', 'TIPO_VINCULO', 'CARGO',
            'CATEGORIA', 'SALARIO', 'FECHA_INGRESO', 'LUGAR_TRABAJO', 'GRUPO_SANGUINEO', 'EMERGENCIA_NOMBRE_1',
            'EMERGENCIA_TELEFONO_1', 'CROQUIS_REFERENCIA'
        }
        for name, field in self.fields.items():
            widget = field.widget
            css = 'form-control'
            if isinstance(widget, forms.CheckboxInput):
                css = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css = 'form-select'
            widget.attrs.setdefault('class', css)
            if name in required_field_names and not isinstance(widget, forms.HiddenInput):
                widget.attrs['required'] = 'required'
                widget.attrs['aria-required'] = 'true'

        if 'EMAIL' in self.fields:
            self.fields['EMAIL'].widget.attrs.setdefault('placeholder', 'usuario@run.gov.py')
            self.fields['EMAIL'].help_text = 'Ingrese su correo institucional. Si escribe solo el usuario, se completará @run.gov.py automáticamente.'

        if 'SALARIO' in self.fields:
            self.fields['SALARIO'].widget = forms.TextInput()
            self.fields['SALARIO'].widget.attrs.update({
                'placeholder': '0',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'data-format-salario': '1',
            })


    def clean_FOTO_CARNET(self):
        foto = self.cleaned_data.get('FOTO_CARNET')
        if foto:
            return foto
        if self.persona and getattr(self.persona, 'FOTO_CARNET', None):
            return self.persona.FOTO_CARNET
        raise forms.ValidationError('Adjunte una foto carnet.')

    def _load_from_instance(self, persona):
        extra = persona.FICHA_EXTRA or {}
        self.initial.update({
            'CI_NUMERO': persona.CI_NUMERO,
            'NOMBRES': persona.NOMBRES,
            'APELLIDOS': persona.APELLIDOS,
            'FECHA_NACIMIENTO': persona.FECHA_NACIMIENTO,
            'ESTADO_CIVIL': persona.ESTADO_CIVIL,
            'TELEFONO': persona.TELEFONO,
            'EMAIL': persona.EMAIL,
            'ACTIVO': persona.ACTIVO,
            'CELULAR': extra.get('CELULAR', ''),
            'DOMICILIO_ACTUAL': extra.get('DOMICILIO_ACTUAL', ''),
            'BARRIO': extra.get('BARRIO', ''),
            'CIUDAD': extra.get('CIUDAD', ''),
            'ALERGIAS_ENFERMEDADES': extra.get('ALERGIAS_ENFERMEDADES', ''),
            'GRUPO_SANGUINEO': extra.get('GRUPO_SANGUINEO', ''),
            'TIENE_SEGURO_MEDICO': extra.get('TIENE_SEGURO_MEDICO', False),
            'SANATORIO': extra.get('SANATORIO', ''),
            'TELEFONO_SANATORIO': extra.get('TELEFONO_SANATORIO', ''),
            'EMERGENCIA_NOMBRE_1': extra.get('EMERGENCIA_NOMBRE_1', ''),
            'EMERGENCIA_TELEFONO_1': extra.get('EMERGENCIA_TELEFONO_1', ''),
            'EMERGENCIA_NOMBRE_2': extra.get('EMERGENCIA_NOMBRE_2', ''),
            'EMERGENCIA_TELEFONO_2': extra.get('EMERGENCIA_TELEFONO_2', ''),
            'NOMBRE_PADRE': extra.get('NOMBRE_PADRE', ''),
            'NOMBRE_MADRE': extra.get('NOMBRE_MADRE', ''),
            'NOMBRE_CONYUGE': extra.get('NOMBRE_CONYUGE', ''),
            'OBSERVACIONES_FICHA': extra.get('OBSERVACIONES_FICHA', ''),
            'CROQUIS_REFERENCIA': extra.get('CROQUIS_REFERENCIA', ''),
            'FIRMA_ACLARACION': extra.get('FIRMA_ACLARACION', ''),
            'FECHA_FIRMA': extra.get('FECHA_FIRMA', ''),
            'NUMERO_DGRP': extra.get('NUMERO_DGRP', ''),
            'FECHA_DGRP': extra.get('FECHA_DGRP', ''),
            'CATEGORIA': extra.get('CATEGORIA', ''),
        })

        try:
            domicilio_actual = persona.domicilios.filter(ES_ACTUAL=True).first()
            if domicilio_actual:
                self.initial.update({
                    'LATITUD': domicilio_actual.LATITUD,
                    'LONGITUD': domicilio_actual.LONGITUD,
                })
        except Exception:
            pass
        for i in range(1, 7):
            self.initial[f'HIJO_{i}_NOMBRE'] = extra.get(f'HIJO_{i}_NOMBRE', '')
            self.initial[f'HIJO_{i}_FECHA'] = extra.get(f'HIJO_{i}_FECHA', '')

        try:
            dl = persona.datos_laborales
            self.initial.update({
                'TIPO_VINCULO': dl.TIPO_VINCULO,
                'NUMERO_DECRETO': dl.NUMERO_DECRETO,
                'FECHA_DECRETO': dl.FECHA_DECRETO,
                'NUMERO_RESOLUCION': dl.NUMERO_RESOLUCION,
                'FECHA_RESOLUCION': dl.FECHA_RESOLUCION,
                'CARGO': dl.CARGO,
                'SALARIO': dl.SALARIO,
                'FECHA_INGRESO': dl.FECHA_INGRESO,
                'LUGAR_TRABAJO': dl.DEPENDENCIA,
            })
        except Exception:
            pass

        try:
            da = persona.datos_academicos
            self.initial.update({
                'CARRERA': da.PROFESION,
                'UNIVERSIDAD': da.UNIVERSIDAD,
                'ANIO_CARRERA': da.ANIO_GRADUACION,
                'NIVEL_PRIMARIO': extra.get('NIVEL_PRIMARIO', False),
                'NIVEL_SECUNDARIO': extra.get('NIVEL_SECUNDARIO', False),
                'NIVEL_UNIVERSITARIO': extra.get('NIVEL_UNIVERSITARIO', False),
                'BACHILLER': extra.get('BACHILLER', ''),
                'ANIO_BACHILLER': extra.get('ANIO_BACHILLER', ''),
                'POSTGRADOS': extra.get('POSTGRADOS', ''),
                'MAESTRIAS': extra.get('MAESTRIAS', ''),
                'DOCTORADOS': extra.get('DOCTORADOS', ''),
                'OTROS_ESTUDIOS': extra.get('OTROS_ESTUDIOS', ''),
            })
        except Exception:
            pass


    def clean_SALARIO(self):
        salario = self.data.get('SALARIO', '') if self.is_bound else self.cleaned_data.get('SALARIO')
        if salario in (None, ''):
            return None
        if isinstance(salario, str):
            normalizado = salario.replace('.', '').replace(' ', '').replace(',', '')
            try:
                return forms.DecimalField(max_digits=12, decimal_places=0).clean(normalizado)
            except forms.ValidationError:
                raise forms.ValidationError('Ingrese un salario válido.')
        return salario

    def clean_EMAIL(self):
        value = (self.cleaned_data.get('EMAIL') or '').strip().lower()
        if not value:
            return value
        if '@' not in value:
            value = f"{value}@run.gov.py"
        return value

    def clean(self):
        cleaned_data = super().clean()

        categoria = cleaned_data.get('CATEGORIA')
        salario = cleaned_data.get('SALARIO')
        fecha_ingreso = cleaned_data.get('FECHA_INGRESO')

        if not categoria:
            self.add_error('CATEGORIA', 'La categoría es obligatoria.')
        if salario in (None, ''):
            self.add_error('SALARIO', 'El salario es obligatorio.')
        if not fecha_ingreso:
            self.add_error('FECHA_INGRESO', 'La fecha de ingreso es obligatoria.')

        tipo = cleaned_data.get('TIPO_VINCULO')

        # Obligatorios condicionales por tipo de vínculo
        if tipo == 'NOMBRADO':
            if not cleaned_data.get('NUMERO_DECRETO'):
                self.add_error('NUMERO_DECRETO', 'Este dato es obligatorio para personal nombrado.')
            if not cleaned_data.get('FECHA_DECRETO'):
                self.add_error('FECHA_DECRETO', 'Este dato es obligatorio para personal nombrado.')
            cleaned_data['NUMERO_RESOLUCION'] = ''
            cleaned_data['FECHA_RESOLUCION'] = None
            cleaned_data['NUMERO_DGRP'] = ''
            cleaned_data['FECHA_DGRP'] = None
        elif tipo == 'CONTRATADO':
            if not cleaned_data.get('NUMERO_RESOLUCION'):
                self.add_error('NUMERO_RESOLUCION', 'Este dato es obligatorio para personal contratado.')
            if not cleaned_data.get('FECHA_RESOLUCION'):
                self.add_error('FECHA_RESOLUCION', 'Este dato es obligatorio para personal contratado.')
            cleaned_data['NUMERO_DECRETO'] = ''
            cleaned_data['FECHA_DECRETO'] = None
            cleaned_data['NUMERO_DGRP'] = ''
            cleaned_data['FECHA_DGRP'] = None
        elif tipo in ('PASANTIA', 'PRACTICANTE'):
            if not cleaned_data.get('NUMERO_DGRP'):
                self.add_error('NUMERO_DGRP', 'Este dato es obligatorio para pasantía o practicantado.')
            if not cleaned_data.get('FECHA_DGRP'):
                self.add_error('FECHA_DGRP', 'Este dato es obligatorio para pasantía o practicantado.')
            cleaned_data['NUMERO_DECRETO'] = ''
            cleaned_data['FECHA_DECRETO'] = None
            cleaned_data['NUMERO_RESOLUCION'] = ''
            cleaned_data['FECHA_RESOLUCION'] = None
        else:
            cleaned_data['NUMERO_DECRETO'] = ''
            cleaned_data['FECHA_DECRETO'] = None
            cleaned_data['NUMERO_RESOLUCION'] = ''
            cleaned_data['FECHA_RESOLUCION'] = None
            cleaned_data['NUMERO_DGRP'] = ''
            cleaned_data['FECHA_DGRP'] = None

        # Al menos un nivel académico
        if not any([
            cleaned_data.get('NIVEL_PRIMARIO'),
            cleaned_data.get('NIVEL_SECUNDARIO'),
            cleaned_data.get('NIVEL_UNIVERSITARIO'),
        ]):
            raise forms.ValidationError('Seleccione al menos un nivel académico alcanzado.')

        if cleaned_data.get('NIVEL_UNIVERSITARIO'):
            if not cleaned_data.get('CARRERA'):
                self.add_error('CARRERA', 'La carrera es obligatoria si marca nivel universitario.')
            if not cleaned_data.get('UNIVERSIDAD'):
                self.add_error('UNIVERSIDAD', 'La universidad es obligatoria si marca nivel universitario.')

        # Si tiene seguro, completar sanatorio
        if cleaned_data.get('TIENE_SEGURO_MEDICO') and not cleaned_data.get('SANATORIO'):
            self.add_error('SANATORIO', 'Indique el sanatorio o seguro correspondiente.')

        return cleaned_data

    def clean_CI_NUMERO(self):
        import re
        ci = self.cleaned_data.get('CI_NUMERO', '').strip()
        if not re.match(r'^[0-9\-]+$', ci):
            raise forms.ValidationError('La cédula solo puede contener números y guiones.')
        qs = Persona.objects.filter(CI_NUMERO=ci)
        if self.persona:
            qs = qs.exclude(pk=self.persona.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una ficha con esa cédula.')
        return ci