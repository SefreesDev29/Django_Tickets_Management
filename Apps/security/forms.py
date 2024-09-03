from django.forms import *
from django import forms
from Apps.security.models import Dashboard

class DashboardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Dashboard
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre del sistema',
                }
            ),
            'author': forms.TextInput(attrs={
                'placeholder': 'Ingrese el autor',
            }),
        }
        exclude = ['user_creation','user_updated']

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
