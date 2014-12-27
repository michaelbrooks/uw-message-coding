from django import forms
from apps.project import models

from django.utils.translation import ugettext_lazy as _

class ProjectCreateForm(forms.ModelForm):
    """
    Form for creating new projects.
    """

    class Meta:
        model = models.Project

        # Choose which fields to show on the form
        fields = ['name', 'description', 'members', 'slug']

        # Customize label text and add help messages
        labels = {
            'slug': _('Short code')
        }

        help_texts = {
            'slug': _('A unique name containing only letters and hyphens (e.g. my-cool-project)')
        }

