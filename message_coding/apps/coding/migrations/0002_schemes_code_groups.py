# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheme',
            name='project',
            field=models.ForeignKey(related_name='schemes', to='project.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='codegroup',
            name='scheme',
            field=models.ForeignKey(related_name='code_groups', to='coding.Scheme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='code_group',
            field=models.ForeignKey(related_name='codes', to='coding.CodeGroup'),
            preserve_default=True,
        ),
    ]
