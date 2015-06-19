# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_remove_task_selection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_coders',
        ),
    ]
