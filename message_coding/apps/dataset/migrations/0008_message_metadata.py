# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0007_auto_20150507_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='metadata',
            field=models.TextField(null=True, blank=True),
        ),
    ]
