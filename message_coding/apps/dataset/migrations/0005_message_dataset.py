# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_dataset_generate_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='dataset',
            field=models.ForeignKey(related_name='messages', to='dataset.Dataset'),
            preserve_default=True,
        ),
    ]
