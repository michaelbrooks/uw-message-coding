from django.views.generic import CreateView, DetailView, TemplateView, FormView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponse, StreamingHttpResponse

from message_coding.apps.dataset import models, forms
from message_coding.apps.coding import models as coding_models
from message_coding.apps.project import models as project_models
from message_coding.apps.base.views import LoginRequiredMixin, ProjectViewMixin
from message_coding.apps.dataset.api import serializers
from message_coding.apps.base.api import UserSerializer
from message_coding.apps.project import api as project_api
from rest_framework.renderers import JSONRenderer

import csv
import codecs



class DatasetDetailView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """View for viewing datasets"""
    model = models.Dataset
    template_name = 'dataset/dataset_detail.html'
    slug_url_kwarg = 'dataset_slug'

    def get_context_data(self, **kwargs):
        # Add some serialized json for bootstrapping the client-side app
        renderer = JSONRenderer()
        kwargs['project_json'] = renderer.render(project_api.ProjectSerializer(self.get_project()).data)
        kwargs['dataset_json'] = renderer.render(serializers.DatasetSerializer(self.object).data)
        kwargs['user_json'] = renderer.render(UserSerializer(self.request.user).data)

        return super(DatasetDetailView, self).get_context_data(**kwargs)


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
            raise e

        return super(DatasetImportView, self).form_valid(form)


class DatasetExportSelectionView(LoginRequiredMixin, ProjectViewMixin, FormView):
    """ View to let user select which tasks to download """

    template_name = "dataset/dataset_export.html"
    form_class = forms.DatasetExportForm


    def get_form_kwargs(self):
        kwargs = super(DatasetExportSelectionView, self).get_form_kwargs()

        # grab the dataset_slug and find relevant tasks
        dataset_slug = self.kwargs["dataset_slug"]
        tasks = project_models.Task.objects.filter(selection__dataset__slug=dataset_slug)

        # add tasks to our form kwargs
        kwargs.update({
            "tasks": tasks
        })

        return kwargs



class DatasetExportView(LoginRequiredMixin, ProjectViewMixin, View):
    """ Simple Export View """

    def get(self, request, project_slug, dataset_slug, **kwargs):
        #models.Message

        # find our dataset & messages
        dataset = models.Dataset.objects.filter(slug=dataset_slug)
        messages = models.Message.objects.filter(dataset=dataset)

        # begin a streaming response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"'%(project_slug, dataset_slug)

        # attach a csv writer to that
        csvwriter = csv.writer(response)
        csvwriter.writerow(["id", "time", "sender", "text", "codes_str"])

        # create a utf-8 encoder
        encoder = codecs.getencoder("utf-8")

        #step through messages
        for m in messages:

            # grab all instances attacahed to this 
            codes = project_models.CodeInstance.objects.filter(message=m)
            codes_str =  u"|".join([unicode(c.code.name) for c in codes]) if codes is not None and codes.count() > 0 else ""

            # create the column values for our row
            cols = [unicode(m.id), unicode(m.time), unicode(m.sender),  unicode(m.text), codes_str]

            # encode and write them
            encoded_cols = [encoder(c)[0] for c in cols]
            csvwriter.writerow(encoded_cols)

        # return the full response
        return response

