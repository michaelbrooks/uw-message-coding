from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.dataset import models


class DatasetImportForm(forms.ModelForm):
    """
    Form for importing a new dataset.
    Handles validating and saving the new Dataset automatically.
    """

    class Meta:
        model = models.Dataset

        # Choose which fields to show on the form
        fields = ['name', 'description', 'slug']

        # Override the contents of the field labels
        labels = {
            'slug': _('Short code')
        }

        # Add help text for some fields
        help_texts = {
            'slug': _('A unique name containing only letters and hyphens (e.g. my-big-dataset)')
        }

