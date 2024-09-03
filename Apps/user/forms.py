from django import forms
from django.forms import ModelForm

from Apps.user.models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

        # Exclude superusers
        if self.instance.pk and self.instance.is_superuser:
            self.fields.pop('is_active')
        
    class Meta:
        model = User
        fields = 'first_name','last_name','email','username','password','image','groups','is_active'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            ),
            'password': forms.PasswordInput(render_value=True,
                                            attrs={
                                                'placeholder': 'Ingrese su password',
                                            }
                                            ),
            'groups': forms.SelectMultiple(attrs={ #custom-select 
                'class': 'form-control select2',
                'style': 'width: 100%',
                'multiple': 'multiple'
            }),
            'is_active': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%'
            }, choices=[(True, 'Activo'),(False, 'Desactivado')])
        }
        exclude = ['user_permissions','last_login','date_joined','is_superuser','is_staff','token']

    def save(self, commit=True):
        data = None
        data_error = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                data = form.save(commit=False)
                if data.pk is None:
                    data.set_password(pwd)
                else:
                    user = User.objects.get(pk=data.pk)
                    if user.password != pwd:
                        data.set_password(pwd)
                data.save()
                data.groups.clear()
                for g in self.cleaned_data['groups']:
                    data.groups.add(g)
            else:
                data_error['error'] = form.errors
                data = data_error
        except Exception as e:
            data_error['error'] = str(e)
            data = data_error
        return data

class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = 'first_name','last_name','email','username','image'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su email',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su username',
                }
            )
        }
        exclude = ['user_permissions','last_login','date_joined','is_superuser','is_active', 'password','is_staff','groups','token']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
