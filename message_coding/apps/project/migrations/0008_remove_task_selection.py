# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_task_dataset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='selection',
        ),
    ]
