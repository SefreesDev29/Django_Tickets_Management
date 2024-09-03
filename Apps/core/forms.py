from datetime import date

from django.forms import *
from django import forms

from crum import get_current_request

from Apps.core.models import Driver, Ticket, Purchase

class TicketForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                }
            ),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio',
            }),
        }
        exclude = ['user_creation','user_updated']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return price

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class DriverForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True
        if not self.instance.pk:
            self.fields['date_birthday'].initial = None
        else:
            request = get_current_request()
            if request.session['group'] == 'Administrador':
                self.fields['dni'].widget.attrs['disabled'] = True
                self.fields['date_birthday'].widget.attrs['disabled'] = True

    class Meta:
        model = Driver
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': forms.DateInput(format='%Y-%m-%d',
                                       attrs={
                                            'type': 'date'
                                       }
                                       ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': forms.Select()
        }
        exclude = ['user_creation','user_updated']

    def clean_date_birthday(self):
        date_birthday = self.cleaned_data['date_birthday']
        if date_birthday > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura.')
        return date_birthday

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driv'].queryset = Driver.objects.none()

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'driv': forms.Select(attrs={
                'class': 'form-control custom-select select2',
            }),
            'date_joined': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    #'value': datetime.now().strftime('%Y-%m-%d'), 
                    'type': 'date',
                    'autocomplete': 'off',
                    'class': 'form-control',
                }
            )
        }
        exclude = ['user_creation','user_updated']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
