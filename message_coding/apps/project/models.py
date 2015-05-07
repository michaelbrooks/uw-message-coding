from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from message_coding.apps.base.models import NameDescriptionMixin, CreatedAtField


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
            if code_instance.code not in applied_codes:
                applied_codes[code_instance.code] = []
            if len(applied_codes[code_instance.code]) < max_examples:
                applied_codes[code_instance.code].append(code_instance.message)
        return applied_codes

    def get_frequency(self):
        code_frequency = {}
        for code_instance in self.code_instances.all():
            if code_instance.code not in code_frequency:
                code_frequency[code_instance.code] = 1
            else:
                code_frequency[code_instance.code]+= 1
        return code_frequency

    def get_coding_summary(self):
        code_groups = self.scheme.code_groups.all()
        code_frequency = {}
        for code_group in code_groups:
            for code in code_group.codes.all():
                code_frequency[code] = {}

        coders = self.assigned_coders.all()
        for coder in coders:
            for code in code_frequency:
                code_frequency[code][coder] = 0

        for code_instance in self.code_instances.all():
            code_frequency[code_instance.code][code_instance.owner] += 1
        return code_frequency

    def get_diff_summary(self):
        """
        code A
        Y\N    | coder1 | coder 2 | coder 3
        coder1 |   x    |   10    |   2
        coder2 |   3*   |   x     |   3
        coder3 |   9    |   0     |   x

        * means there are 3 messages that coder2 label coder A but coder1 does not

        :param:
        :return:
        """

        code_groups = self.scheme.code_groups.all()
        code_diff_matrix = {}
        for code_group in code_groups:
            for code in code_group.codes.all():
                diff_matrix = {}
                coders = self.assigned_coders.all()
                for coder1 in coders:
                    diff_matrix[coder1] = {}
                    for coder2 in coders:
                        diff_matrix[coder1][coder2] = 0

                msgs = self.selection.get_messages()
                code_table = {}
                for msg in msgs:
                    code_table[msg.pk] = {}
                    for coder in coders:
                        code_table[msg.pk][coder] = 0

                for code_instance in self.code_instances.filter(code=code).all():
                    try:
                        code_table[code_instance.message.pk][code_instance.owner] += 1
                    except:
                        continue


                for msg in msgs:
                    for coder1 in coders:
                        for coder2 in coders:
                            if coder1 == coder2:
                                continue

                            if code_table[msg.pk][coder1] and not code_table[msg.pk][coder2]:
                                diff_matrix[coder1][coder2] += 1


                code_diff_matrix[code] = diff_matrix


        return code_diff_matrix

class CodeInstance(models.Model):
    """A code applied to a data point in the context of a task"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="code_instances")
    task = models.ForeignKey(Task, related_name='code_instances')
    message = models.ForeignKey('dataset.Message', related_name='code_instances')
    code = models.ForeignKey('coding.Code', related_name='instances')
