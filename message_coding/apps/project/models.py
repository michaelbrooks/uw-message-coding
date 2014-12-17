from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin, CreatedAtField


class Project(NameDescriptionMixin):

    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # People who belong to this project
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')


class Task(NameDescriptionMixin):
    """Defines a coding task: a group of coders, a selection of data, and a coding scheme"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks_owned")

    project = models.ForeignKey('project.Project')
    selection = models.ForeignKey('dataset.Selection')
    scheme_version = models.ForeignKey('coding.SchemeVersion')
    assigned_coders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks_assigned')
