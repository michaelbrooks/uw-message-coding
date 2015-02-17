# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from message_coding.apps.project.models import slug_validator

class Migration(migrations.Migration):
    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=None, unique=True, validators=[slug_validator]),
            preserve_default=False,
        ),
    ]
