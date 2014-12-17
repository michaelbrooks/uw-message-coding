# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', base.models.CreatedAtField(auto_now=True)),
                ('code', models.ForeignKey(related_name='instances', to='coding.Code')),
                ('message', models.ForeignKey(related_name='code_instances', to='dataset.Message')),
                ('owner', models.ForeignKey(related_name='code_instances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('created_at', base.models.CreatedAtField(auto_now=True)),
                ('members', models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('created_at', base.models.CreatedAtField(auto_now=True)),
                ('assigned_coders', models.ManyToManyField(related_name='tasks_assigned', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='tasks_owned', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='project.Project')),
                ('scheme', models.ForeignKey(to='coding.Scheme')),
                ('selection', models.ForeignKey(to='dataset.Selection')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='codeinstance',
            name='task',
            field=models.ForeignKey(related_name='code_instances', to='project.Task'),
            preserve_default=True,
        ),
    ]
