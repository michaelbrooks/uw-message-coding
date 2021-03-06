from django import forms
from django.utils.translation import ugettext_lazy as _

from message_coding.apps.project import models


class ProjectForm(forms.ModelForm):
    """
    Form for creating new projects.
    """

    class Meta:
        model = models.Project

        # Choose which fields to show on the form
        fields = ['name', 'slug', 'description', 'members']

        # Customize label text and add help messages
        labels = {
            'slug': _('Short code')
        }
        help_texts = {
            'slug': _('A unique name containing only letters and hyphens (e.g. my-cool-project)')
        }

