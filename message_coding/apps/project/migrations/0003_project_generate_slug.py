# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify


def generate_slug(apps, schema_editor):
    Project = apps.get_model('project.Project')
    for project in Project.objects.filter(slug=''):
        project.slug = slugify(project.name)
        project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_add_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slug)
    ]
