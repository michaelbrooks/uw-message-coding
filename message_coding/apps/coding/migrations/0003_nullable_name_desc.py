# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0002_schemes_code_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='code',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='codegroup',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='codegroup',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scheme',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scheme',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
    ]
