from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin


class Scheme(NameDescriptionMixin):
    created_at = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey('project.Project', related_name="schemes")


class SchemeVersion(NameDescriptionMixin):
    """A version of a coding scheme"""

    scheme = models.ForeignKey(Scheme, related_name='versions')
    created_at = models.DateTimeField()
    number = models.PositiveIntegerField()


class CodeGroup(NameDescriptionMixin):
    """Defines a group of related codes"""
    scheme_version = models.ForeignKey(SchemeVersion, related_name="code_groups")


class Code(NameDescriptionMixin):
    """Defines a single code"""
    scheme_version = models.ForeignKey(SchemeVersion, related_name="codes")
    code_group = models.ForeignKey(CodeGroup, related_name="codes")


class Task(NameDescriptionMixin):
    """Defines a coding task: a group of coders, a selection of data, and a coding scheme"""
    created_at = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks_owned")

    selection = models.ForeignKey('dataset.Selection')
    scheme_version = models.ForeignKey(SchemeVersion)
    assigned_coders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks_assigned')