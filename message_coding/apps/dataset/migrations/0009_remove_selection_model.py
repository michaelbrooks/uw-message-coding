# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_remove_task_selection'),
        ('dataset', '0008_message_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selection',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='selection',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Selection',
        ),
    ]
