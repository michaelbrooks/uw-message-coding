from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin

class Project(NameDescriptionMixin):

    created_at = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # People who belong to this project
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')


