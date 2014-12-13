from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin, CreatedAtField


class Project(models.Model):

    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # People who belong to this project
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')


