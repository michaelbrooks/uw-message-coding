from django.db import models

class NameDescriptionMixin(models.Model):
    """Inherit from this to add name/description fields"""

    class Meta:
        abstract = True

    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(default='')


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class CreatedAtField(models.DateTimeField):
    """A datetime field that auto-nows automatically"""

    def __init__(self, *args, **kwargs):
        kwargs['auto_now'] = True
        kwargs['editable'] = False
        super(CreatedAtField, self).__init__(*args, **kwargs)
