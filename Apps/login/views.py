from datetime import datetime,timedelta
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.utils.timezone import make_aware
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
# from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect,JsonResponse
# from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from Apps.login.forms import ResetPasswordForm, ChangePasswordForm
from Apps.user.models import User
from Apps.security.models import AccessUser


class LoginFormView(LoginView):
    template_name = 'login/login.html'
    success_url = reverse_lazy('core:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    last_failed_access = AccessUser.objects.filter(
                        user=user,
                        is_success=False
                    ).order_by('-timestamp').first()

                    if last_failed_access:
                        if (last_failed_access.timestamp - timedelta(hours=5)).date() < datetime.now().date():
                            user.is_active = True
                            user.save()
                except User.DoesNotExist:
                    pass
        # if request.user.is_authenticated:
        #     return redirect('core:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     user = form.get_user()
    #     AccessUser(user=user).save()
    #     return response
    
    # def form_invalid(self, form):
    #     username = form.data.get('username')
    #     try:
    #         user = User.objects.get(username=username)

    #         start_datetime = make_aware(datetime.combine(timezone.now().date(), datetime.min.time()))
    #         end_datetime = make_aware(datetime.combine(timezone.now().date(), datetime.max.time()))
    #         failed_attempts_today = AccessUser.objects.filter(
    #             user=user,
    #             is_success=False,
    #             timestamp__range=[start_datetime,end_datetime]
    #         ).count()

    #         AccessUser.objects.create(user=user, is_success=False)

    #         if failed_attempts_today > 2:  
    #             user.is_active = False
    #             user.save()
    #             messages.error(self.request, 'Tu cuenta ha sido bloqueada por demasiados intentos fallidos. Contacta al administrador.')
    #         else:
    #             if user.is_active:
    #                 remaining_attempts = 3 - failed_attempts_today
    #                 messages.error(self.request, f"Contraseña incorrecta. Te queda {remaining_attempts} {'intentos' if remaining_attempts>1 else 'intento'}.")
    #             else:
    #                 messages.error(self.request, 'Tu cuenta ha sido bloqueada por demasiados intentos fallidos. Contacta al administrador.')
    #     except User.DoesNotExist:
    #         pass
    #     return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'validate_access':
                form = self.get_form()
                if form.is_valid():
                    user = form.get_user()
                    login(request, user)
                    AccessUser(user=user).save()
                else:
                    username = form.cleaned_data.get('username')
                    user = User.objects.filter(username=username).first()
                    if user:
                        start_datetime = make_aware(datetime.combine(datetime.now().date(), datetime.min.time()))
                        end_datetime = make_aware(datetime.combine(datetime.now().date(), datetime.max.time()))
                        failed_attempts_filter = AccessUser.objects.filter(
                            user=user,
                            is_success=False,
                            timestamp__range=[start_datetime, end_datetime]
                        )
                        last_access_user = AccessUser.objects.filter(user=user,is_success=True).order_by('id').last()
                        if last_access_user:
                            failed_attempts_filter = failed_attempts_filter.filter(id__gt=last_access_user.id)
                        failed_attempts_today = failed_attempts_filter.count()
                        AccessUser.objects.create(user=user, is_success=False)
                        if failed_attempts_today > 2:  
                            user.is_active = False
                            user.save()
                            data['error'] =  'Tu cuenta ha sido bloqueada por demasiados intentos fallidos. Contacta al administrador.'
                        else:
                            if user.is_active:
                                remaining_attempts = 3 - failed_attempts_today
                                data['error'] =  f"Contraseña incorrecta. Te queda {remaining_attempts} {'intentos' if remaining_attempts>1 else 'intento'}."
                            else:
                                data['error'] = 'Tu cuenta ha sido bloqueada por demasiados intentos fallidos. Contacta al administrador.'
                    else:
                        data['error'] = 'Credenciales inválidas, usuario no se encuentra registrado.'
            else:
                data['error'] = 'No ha ingresado a ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        context['action'] = 'validate_access'
        context['menu_url'] = self.success_url
        return context

class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'login/resetpwd.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_pwd(self, user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = formataddr(('Soporte App', settings.EMAIL_HOST_USER)) 
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'

            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/change/password/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}/login/'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)  # self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'login/changepwd.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambio de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context
