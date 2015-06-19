# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0004_auto_20150507_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codegroup',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
