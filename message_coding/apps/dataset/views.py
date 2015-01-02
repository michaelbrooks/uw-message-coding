from django.views.generic import CreateView, DetailView
from django.core.urlresolvers import reverse

from apps.dataset import models, forms
from base.views import LoginRequiredMixin, ProjectViewMixin

import csv
import codecs



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


        f = form.cleaned_data['import_file']

        # run it through codecs, if we don't some files will not be read properly 
        # because django has already "opened" their files and not with universal newlines
        cf = codecs.EncodedFile(f, "utf-8")

        # do import
        try:
            reader = csv.DictReader(cf)
            for row in reader:
                #print row
                text = row['text'] if 'text' in row else None
                sender = row['sender'] if 'sender' in row else None
                time = row['time'] if 'time' in row else None

                if text is not None:
                    msg = models.Message.objects.create(dataset=form.instance, text=text, sender=sender, time=time)
                    msg.save()

        except Exception, e:
            print "!!!!\n"*4
            print "Exception occurred", e




        return super(DatasetImportView, self).form_valid(form)
