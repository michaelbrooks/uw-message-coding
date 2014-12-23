from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin, CreatedAtField
from django.core.urlresolvers import reverse


class Dataset(NameDescriptionMixin):
    """Defines a dataset imported into a project by a user."""

    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    projects = models.ManyToManyField('project.Project', related_name='datasets')
    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('dataset', kwargs={
            'pk': self.pk,
        })



class Selection(models.Model):
    """Defines a subset of a dataset"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    dataset = models.ForeignKey(Dataset)

    type = models.CharField(max_length=150)
    selection = models.BinaryField()


class Message(models.Model):
    """A single message in a dataset"""

    dataset = models.ForeignKey(Dataset, related_name='messages')

    sender = models.CharField(max_length=250)
    time = models.DateTimeField()
    text = models.TextField()

