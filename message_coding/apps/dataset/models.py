from django.db import models
from django.conf import settings

from base.models import NameDescriptionMixin, CreatedAtField
from django.core.exceptions import ValidationError
import json

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


class Selection(models.Model):
    """Defines a subset of a dataset"""
    created_at = CreatedAtField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    dataset = models.ForeignKey(Dataset)

    type = models.CharField(max_length=150)
    selection = models.BinaryField()

    def get_messages(self):
        from apps.dataset.filters import Selector
        selector = Selector(type=self.type, data=self.selection)
        return selector.filter(self.dataset.messages.all)

    def size(self):
        return self.get_messages().count()


class Message(models.Model):
    """A single message in a dataset"""

    dataset = models.ForeignKey(Dataset, related_name='messages')

    sender = models.CharField(max_length=250)
    time = models.DateTimeField()
    text = models.TextField()

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
