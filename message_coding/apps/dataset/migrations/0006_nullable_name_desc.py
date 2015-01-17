# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0005_message_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
    ]
