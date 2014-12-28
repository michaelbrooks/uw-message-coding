# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.dataset.models


class Migration(migrations.Migration):
    dependencies = [
        ('dataset', '0002_dataset_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='slug',
            field=models.SlugField(default=None, unique=True, validators=[apps.dataset.models.slug_validator]),
            preserve_default=False,
        ),
    ]
