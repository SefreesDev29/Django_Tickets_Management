from datetime import datetime
from datetime import timedelta 

from django.db import models
from django.forms import model_to_dict
from django.conf import settings

from crum import get_current_user
from simple_history.models import HistoricalRecords

from Apps.utils import gender_choices
from Apps.models import BaseModel
from Apps.security.validators import validate_file_size

class Ticket(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    price = models.DecimalField(default=1.00, max_digits=9, decimal_places=2, verbose_name='Precio')

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
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    def toJSON(self):
        item = model_to_dict(self)
        item['price'] = format(self.price, '.2f')
        date_creation = self.date_creation - timedelta(hours=5)
        item['user_create'] = self.user_creation.toJSON()
        item['date_create'] = date_creation.strftime('%d/%m/%Y %H:%M')
        item['date_update'] = '-'
        item['user_update'] = {'full_name': '-'}
        if self.user_updated:
            date_updated = self.date_updated - timedelta(hours=5)
            item['date_update'] = date_updated.strftime('%d/%m/%Y %H:%M')
            item['user_update'] = self.user_updated.toJSON()
        return item

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['id']

class Driver(BaseModel):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=8, verbose_name='Dni', unique=True)
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')
    history = HistoricalRecords()

    def __str__(self):
        return self.get_full_name()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None and str(user) != 'AnonymousUser':
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        self.full_clean()
        super(Driver, self).save(force_insert, force_update, using, update_fields)

    def get_full_name(self):
        return '{} {}'.format(self.names, self.surnames)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%d/%m/%Y')
        item['full_name'] = self.get_full_name()
        date_creation = self.date_creation - timedelta(hours=5)
        item['user_create'] = self.user_creation.toJSON()
        item['date_create'] = date_creation.strftime('%d/%m/%Y %H:%M')
        item['date_update'] = (self.date_updated - timedelta(hours=5)).strftime('%d/%m/%Y %H:%M') if self.user_updated else '-'
        item['user_update'] = self.user_updated.toJSON() if self.user_updated else {'username': '-', 'full_name': '-'}
        return item

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
        ordering = ['id']

class Purchase(BaseModel):
    driv = models.ForeignKey(Driver, on_delete=models.PROTECT, verbose_name='Chofer Asociado')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Compra')
    file = models.FileField(upload_to='files', null=True, blank=True, validators=[validate_file_size], verbose_name='Documento')
    history = HistoricalRecords()
    
    def __str__(self):
        return self.driv.names
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None and str(user) != 'AnonymousUser':
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        self.full_clean()
        super(Purchase, self).save(force_insert, force_update, using, update_fields)
    
    def get_file(self):
        if self.file:
            return '{}{}'.format(settings.MEDIA_URL, self.file)
        return '{}{}'.format(settings.STATIC_URL, 'img/FileEmpty.pdf')

    def toJSON(self):
        item = model_to_dict(self)
        item['driv'] = self.driv.toJSON()
        item['file'] = self.get_file()
        item['date_joined'] = self.date_joined.strftime('%d/%m/%Y')
        item['det'] = [i.toJSON() for i in self.detpurchase_set.all()]
        date_creation = self.date_creation - timedelta(hours=5)
        item['user_create'] = self.user_creation.toJSON()
        item['date_create'] = date_creation.strftime('%d/%m/%Y %H:%M')
        item['date_update'] = '-'
        item['user_update'] = {'full_name': '-'}
        if self.user_updated:
            date_updated = self.date_updated - timedelta(hours=5)
            item['date_update'] = date_updated.strftime('%d/%m/%Y %H:%M')
            item['user_update'] = self.user_updated.toJSON()
        return item

    def delete(self, using=None, keep_parents=False):
        for det in self.detpurchase_set.all():
            det.prod.save()
        super(Purchase, self).delete()

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ['-id'] 

class DetPurchase(BaseModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    prod = models.ForeignKey(Ticket, on_delete=models.PROTECT, verbose_name='Ticket')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    serieinicial = models.IntegerField(default=0, verbose_name='SerieInicial')
    seriefinal = models.IntegerField(default=0, verbose_name='SerieFinal')
    history = HistoricalRecords()

    def __str__(self):
        return self.prod.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None and str(user) != 'AnonymousUser':
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        self.full_clean()
        super(DetPurchase, self).save(force_insert, force_update, using, update_fields)

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['prod'] = self.prod.toJSON()
        return item

    class Meta:
        verbose_name = 'Purchase Detail'
        verbose_name_plural = 'Purchases Details'
        ordering = ['id']
