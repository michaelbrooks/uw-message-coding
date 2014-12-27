# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.project.models

class Migration(migrations.Migration):
    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=None, unique=True, validators=[apps.project.models.slug_validator]),
            preserve_default=False,
        ),
    ]
