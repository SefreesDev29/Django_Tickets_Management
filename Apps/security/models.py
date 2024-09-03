from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from crum import get_current_user,get_current_request

from Apps.models import BaseModel
from Apps.security.utils import interv_choice_graph_barline, grade_choice_graph_circular
from Apps.security.validators import validate_image_size_only,validate_image_size_and_dimensions

class AccessUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=45, verbose_name='IP', null=True, blank=True)
    user_agent = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.ip_address
    
    def save(self, *args, **kwargs):
        request = get_current_request()
        if request:
            self.ip_address = request.META.get('REMOTE_ADDR')
            self.user_agent = request.user_agent
        super(AccessUser, self).save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['timestamp'] = (self.timestamp - timedelta(hours=5)).strftime('%d/%m/%Y %H:%M:%S')
        return item

    class Meta:
        verbose_name = 'AccessUser'
        verbose_name_plural = 'AccessUsers'
        default_permissions = ()
        permissions = (
            ('view_accessuser', 'Can view AccessUser'),
            ('delete_accessuser', 'Can delete AccessUser')
        )
        ordering = ['-id'] 

class Dashboard(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    author = models.CharField(max_length=150, verbose_name='Autor')
    logo = models.ImageField(upload_to='logos', null=True, blank=True, verbose_name='Logo', validators=[validate_image_size_and_dimensions])
    background = models.ImageField(upload_to='backgrounds', null=True, blank=True, verbose_name='Fondo', validators=[validate_image_size_only])
    interv_graph_barline = models.IntegerField(choices=interv_choice_graph_barline, default=1, verbose_name='Intervalo Gráfico de Barras y Lineal')
    grade_graph_circular = models.IntegerField(choices=grade_choice_graph_circular, default=360, verbose_name='Grados Gráfico Circular')

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None and str(user) != 'AnonymousUser':
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        self.full_clean()
        super(Dashboard, self).save(force_insert, force_update, using, update_fields)
    
    def get_logo(self):
        if self.logo:
            return '{}{}'.format(settings.MEDIA_URL, self.logo)
        return '{}{}'.format(settings.STATIC_URL, 'img/logoweb.png')
    
    def get_background(self):
        if self.background:
            return '{}{}'.format(settings.MEDIA_URL, self.background)
        return '{}{}'.format(settings.STATIC_URL, 'img/Centro.jpg')

    def toJSON(self):
        item = model_to_dict(self)
        item['logo'] = self.get_logo()
        item['background'] = self.get_background()
        return item

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['id'] 
