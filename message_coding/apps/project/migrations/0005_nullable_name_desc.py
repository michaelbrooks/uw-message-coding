# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_task_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(related_name='projects_owned', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_coders',
            field=models.ManyToManyField(default=None, related_name='tasks_assigned', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(default=b'', max_length=150),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='scheme',
            field=models.ForeignKey(default=None, to='coding.Scheme', null=True),
            preserve_default=True,
        ),
    ]
