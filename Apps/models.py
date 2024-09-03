from django.db import models
from django.conf import settings
from Apps.user.models import User


class BaseModel(models.Model):
    user_creation = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_creation',
                                      null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_cupdated',
                                      null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
