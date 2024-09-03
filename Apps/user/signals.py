import threading

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.contrib.auth.models import Group, Permission
from django.conf import settings

from Apps.user.models import User

class EmailThread(threading.Thread):
    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run(self):
        try:
            subject = 'Bienvenido al Sistema de Boletería!'
            from_email = f'Soporte App <{settings.EMAIL_HOST_USER}>'
            recipient_list = [self.instance.email]

            context = {
                'user': self.instance, 
                'link_resetpwd': '{}/login/reset/password/'.format(settings.DOMAIN)
            }
            message = render_to_string('user/send_email.html', context)

            email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
            email.content_subtype = 'html'
            email.send(fail_silently=False)
        except BadHeaderError:
            print('Invalid header found.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

@receiver(post_save, sender=User)
def send_welcome_user(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            admin_group, createdadmin = Group.objects.get_or_create(name='Administrador')
            if createdadmin:
                permissions = Permission.objects.all()
                admin_group.permissions.set(permissions)
            instance.groups.add(admin_group)

            driver_group, createdriver = Group.objects.get_or_create(name='Chofer')
            if createdriver:
                detpurchase_permissions = Permission.objects.filter(content_type__model='detpurchase')
                driver_group.permissions.add(*detpurchase_permissions)

                purchase_view_change_create_permissions = Permission.objects.filter(
                    content_type__model='purchase',
                    codename__in=['view_purchase', 'change_purchase', 'add_purchase']
                )
                driver_group.permissions.add(*purchase_view_change_create_permissions)
        else:
            email_thread = EmailThread(instance)
            email_thread.start()