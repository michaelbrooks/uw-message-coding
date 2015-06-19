# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def copy_dataset_from_selection(apps, schema_editor):
    Task = apps.get_model('project.Task')
    for task in Task.objects.all():
        task.dataset = task.selection.dataset
        task.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0008_message_metadata'),
        ('project', '0006_auto_20150507_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dataset',
            field=models.ForeignKey(related_name='tasks', default=None, to='dataset.Dataset'),
            preserve_default=False,
        ),
        migrations.RunPython(copy_dataset_from_selection),
    ]
