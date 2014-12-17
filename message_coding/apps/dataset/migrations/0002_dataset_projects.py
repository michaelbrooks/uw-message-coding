# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='projects',
            field=models.ManyToManyField(related_name='datasets', to='project.Project'),
            preserve_default=True,
        ),
    ]
