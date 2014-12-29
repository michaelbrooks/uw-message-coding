from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse

from apps.dataset import models, forms
from base.views import LoginRequiredMixin, ProjectViewMixin


class DatasetDetailView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing datasets"""
    model = models.Dataset
    template_name = 'dataset/dataset_detail.html'
    slug_url_kwarg = 'dataset_slug'


class DatasetImportView(LoginRequiredMixin, ProjectViewMixin, CreateView):
    """View for importing a dataset """

    form_class = forms.DatasetImportForm
    template_name = "dataset/dataset_import.html"

    def get_success_url(self):
        return reverse('dataset', kwargs={
            'project_slug': self.get_project().slug,
            'dataset_slug': self.object.slug,
        })

    def form_valid(self, form):
        # The user comes from the session
        form.instance.owner = self.request.user

        # This comes from the URL
        project = self.get_project()
        form.instance.save()
        form.instance.projects.add(project)

        return super(DatasetImportView, self).form_valid(form)
