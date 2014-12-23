
from django.views.generic import CreateView, DetailView

import models
from django.apps import apps
from apps.dataset import models as dataset_models
from django.http import HttpResponse
from django.template import Context,loader
from base.views import LoginRequiredMixin


class DatasetDetailView(LoginRequiredMixin,DetailView):
    """View for viewing datasets"""
    model = models.Dataset
    template_name = 'dataset/dataset_detail.html'

