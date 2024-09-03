from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from datetime import timedelta 

from django.conf import settings


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/avatar.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions'])
        if self.last_login:
            fecha = self.last_login - timedelta(hours=5)
            item['last_login'] = fecha.strftime('%d/%m/%Y %H:%M')
        fecha1 = self.date_joined - timedelta(hours=5)
        item['date_joined'] = fecha1.strftime('%d/%m/%Y %H:%M')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    class Meta:
        ordering = ['id']