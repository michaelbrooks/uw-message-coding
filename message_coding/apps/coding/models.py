from django.db import models
from django.conf import settings

from message_coding.apps.base.models import NameDescriptionMixin, CreatedAtField


class Scheme(NameDescriptionMixin):
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    project = models.ForeignKey('project.Project', related_name="schemes")


class CodeGroup(NameDescriptionMixin):
    """Defines a group of related codes"""
    scheme = models.ForeignKey(Scheme, related_name="code_groups")
    order = models.PositiveIntegerField()


class Code(NameDescriptionMixin):
    """Defines a single code"""
    code_group = models.ForeignKey(CodeGroup, related_name="codes")
    order = models.PositiveIntegerField()
