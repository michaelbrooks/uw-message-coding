# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0006_auto_20150619_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='name',
            field=models.CharField(default=b'', max_length=150),
        ),
        migrations.AlterField(
            model_name='codegroup',
            name='name',
            field=models.CharField(default=b'', max_length=150),
        ),
        migrations.AlterField(
            model_name='scheme',
            name='name',
            field=models.CharField(default=b'', max_length=150),
        ),
    ]
