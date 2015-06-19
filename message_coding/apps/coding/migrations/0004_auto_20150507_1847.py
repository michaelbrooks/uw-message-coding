# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0003_nullable_name_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='codegroup',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='scheme',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
