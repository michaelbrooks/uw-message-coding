from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from message_coding.apps.dataset import models
import message_coding.apps.project.models as project_models


class DatasetImportForm(forms.ModelForm):
    """
    Form for importing a new dataset.
    Handles validating and saving the new Dataset automatically.
    """

    import_file = forms.FileField()

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



class DatasetExportForm(forms.Form):
    """
    Form for exporting a dataset.
    Handles selecting for
    """

    tasks = forms.ModelMultipleChoiceField(
        label="Tasks to export", 
        help_text="Select all tasks you want to export. Hold shift to select multiple items",
        widget=forms.SelectMultiple, 
        queryset=None)

    def __init__(self, *args, **kwargs):
        print "init - args", args
        print "init - kwargs", kwargs
        selected_tasks = kwargs.pop("tasks", [])
        super(DatasetExportForm, self).__init__(*args, **kwargs)

        self.fields["tasks"].queryset = project_models.Task.objects.filter(pk__in=selected_tasks)


