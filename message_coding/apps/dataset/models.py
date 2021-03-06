from django.db import models
from django.conf import settings

from message_coding.apps.base.models import NameDescriptionMixin, CreatedAtField
from django.core.exceptions import ValidationError
import json
from django.db.models import Min, Max
from message_coding.apps.dataset.filters import MessageFilter

# These strings cannot be dataset slugs
illegal_dataset_slugs = (
    'import',
)


def slug_validator(value):
    if value in illegal_dataset_slugs:
        raise ValidationError("%s cannot be used as a dataset code" % value)


class Dataset(NameDescriptionMixin):
    """Defines a dataset imported into a project by a user."""

    slug = models.SlugField(unique=True, validators=[slug_validator])
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    projects = models.ManyToManyField('project.Project', related_name='datasets')
    @property
    def min_time(self):
        result = self.messages.all().aggregate(Min('time'))
        if result:
            return result['time__min']
    @property
    def max_time(self):
        result = self.messages.all().aggregate(Max('time'))
        if result:
            return result['time__max']        


class Message(models.Model):
    """A single message in a dataset"""

    dataset = models.ForeignKey(Dataset, related_name='messages')

    sender = models.CharField(max_length=250)
    time = models.DateTimeField()
    text = models.TextField()
    metadata = models.TextField(blank=True, null=True)

    def has_image(self):
        return self.image_src() is not None

    def image_src(self):
        import re
        m = re.search(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})[\/\w\.-]*\.(jpg|png|gif)?', self.text)
        if m:
            print m.groups()
            return m.group(0)
        return None

    def text_without_image(self):
        src = self.image_src()
        text = self.text

        if src:
            start = text.find(src)
            text = text[0:start] + text[start+len(src):]

        return text

    def __unicode__(self):
        return str(self.pk) + self.text
