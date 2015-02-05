from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from base.models import NameDescriptionMixin, CreatedAtField


# These strings cannot be project slugs
illegal_project_slugs = (
    'admin',
    'project',
    'accounts',
    'user_dash',
    'api',
)


def slug_validator(value):
    if value in illegal_project_slugs:
        raise ValidationError("%s cannot be used as a project code" % value)


class Project(NameDescriptionMixin):
    slug = models.SlugField(unique=True, validators=[slug_validator])
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects_owned')

    # People who belong to this project
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')

    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('project', kwargs={
            'project_slug': self.slug,
        })

    def has_member(self, user):
        return self.members.filter(pk=user.pk)


class Task(NameDescriptionMixin):
    """Defines a coding task: a group of coders, a selection of data, and a coding scheme"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks_owned")

    project = models.ForeignKey('project.Project', related_name="tasks")
    selection = models.ForeignKey('dataset.Selection')
    scheme = models.ForeignKey('coding.Scheme', default=None, null=True)
    assigned_coders = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks_assigned', default=None, null=True)

    def get_absolute_url(self):
        """What is the main url for this object"""
        return reverse('task', kwargs={
            'task_pk': self.pk,
            'project_slug': self.project.slug,
        })

    def is_assigned_to(self, user):
        return self.assigned_coders.filter(pk=user.pk)
        
    def get_examples(self,max_examples=5):
        applied_codes = {}
        for code_instance in self.code_instances.all():
            if code_instance not in applied_codes:
                applied_codes[code_instance.code] = []
            if len(applied_codes[code_instance.code]) < max_examples:
                applied_codes[code_instance.code].append(code_instance.message)   
				
	return applied_codes


class CodeInstance(models.Model):
    """A code applied to a data point in the context of a task"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="code_instances")
    task = models.ForeignKey(Task, related_name='code_instances')
    message = models.ForeignKey('dataset.Message', related_name='code_instances')
    code = models.ForeignKey('coding.Code', related_name='instances')
    