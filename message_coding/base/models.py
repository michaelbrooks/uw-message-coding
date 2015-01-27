from django.db import models

# Use get_user_model() to get the user model
# i.e. do not import django.contrib.auth.models.User directly!
# You can also use settings.AUTH_USER_MODEL, in ForeignKeys for example.
from django.contrib.auth import get_user_model
from django.conf import settings


class NameDescriptionMixin(models.Model):
    """Inherit from this to add name/description fields"""

    class Meta:
        abstract = True

    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')


    def __str__(self):
    	return self.name

    def __unicode__(self):
    	return self.name


class CreatedAtField(models.DateTimeField):
    """A datetime field that auto-nows automatically"""

    def __init__(self, *args, **kwargs):
        kwargs['auto_now'] = True
        super(CreatedAtField, self).__init__(*args, **kwargs)
