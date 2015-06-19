# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_nullable_name_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_coders',
            field=models.ManyToManyField(default=None, related_name='tasks_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
