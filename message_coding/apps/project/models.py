from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin, CreatedAtField
from django.core.urlresolvers import reverse

class Project(NameDescriptionMixin):

    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    # People who belong to this project
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    
    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('project', kwargs={
            'pk': self.pk,
        })


class Task(NameDescriptionMixin):
    """Defines a coding task: a group of coders, a selection of data, and a coding scheme"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks_owned")

    project = models.ForeignKey('project.Project', related_name="tasks")
    selection = models.ForeignKey('dataset.Selection')
    scheme = models.ForeignKey('coding.Scheme')
    assigned_coders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks_assigned')

    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('project_task', kwargs={
            'pk': self.pk,
            'project_pk': self.project.pk,
        })


class CodeInstance(models.Model):
    """A code applied to a data point in the context of a task"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="code_instances")
    task = models.ForeignKey(Task, related_name='code_instances')

    message = models.ForeignKey('dataset.Message', related_name='code_instances')
    code = models.ForeignKey('coding.Code', related_name='instances')
