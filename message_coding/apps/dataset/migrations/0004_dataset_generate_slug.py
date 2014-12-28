# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.utils.text import slugify


def generate_slug(apps, schema_editor):
    Dataset = apps.get_model('dataset.Dataset')
    for dataset in Dataset.objects.filter(slug=''):
        dataset.slug = slugify(dataset.name)
        dataset.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dataset', '0003_dataset_add_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slug),
    ]
