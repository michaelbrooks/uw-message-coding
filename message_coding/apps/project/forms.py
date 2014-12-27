from django import forms
from apps.project import models

from django.utils.translation import ugettext_lazy as _

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name', 'description', 'members', 'slug']
        labels = {
            'slug': _('Short code')
        }
        help_texts = {
            'slug': _('A unique name containing only letters and hyphens (e.g. my-cool-project)')
        }

