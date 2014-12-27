from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.dataset import models


class DatasetImportForm(forms.ModelForm):
    class Meta:
        model = models.Dataset
        fields = ['name', 'description', 'slug']
        labels = {
            'slug': _('Short code')
        }
        help_texts = {
            'slug': _('A unique name containing only letters and hyphens (e.g. my-big-dataset)')
        }

