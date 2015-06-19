# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_remove_task_assigned_coders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'', max_length=150),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(default=b'', max_length=150),
        ),
    ]
