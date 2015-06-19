from django.views.generic import CreateView, DetailView, FormView, View
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from message_coding.apps.dataset import models, forms
from message_coding.apps.coding import models as coding_models
from message_coding.apps.project import models as project_models
from message_coding.apps.base.views import LoginRequiredMixin, ProjectViewMixin

from message_coding.apps.api import serializers

from rest_framework.renderers import JSONRenderer

import csv
import codecs
import urllib
from datetime import datetime



class DatasetDetailView(LoginRequiredMixin, ProjectViewMixin, DetailView):
    """
    View for viewing datasets
    """

    model = models.Dataset
    template_name = 'dataset/dataset_detail.html'
    slug_url_kwarg = 'dataset_slug'

    def get_context_data(self, **kwargs):
        # Add some serialized json for bootstrapping the client-side app
        renderer = JSONRenderer()
        kwargs['project_json'] = renderer.render(serializers.ProjectSerializer(self.get_project()).data)
        kwargs['dataset_json'] = renderer.render(serializers.DatasetSerializer(self.object).data)
        kwargs['user_json'] = renderer.render(serializers.UserSerializer(self.request.user).data)

        return super(DatasetDetailView, self).get_context_data(**kwargs)


class DatasetImportView(LoginRequiredMixin, ProjectViewMixin, CreateView):
    """
    View for importing a dataset
    """

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

            # grab our fields
            standard_fieldnames = set(['text', 'sender', 'time'])
            fieldnames = set(reader.fieldnames)

            fieldnames -= standard_fieldnames


            for row in reader:
                #print row
                text = row['text'] if 'text' in row else None
                sender = row['sender'] if 'sender' in row else None
                time = row['time'] if 'time' in row else None

                print "import time - (%s)"%(time)

                if len(fieldnames) > 0:
                    metadata = {}
                    for fieldname in fieldnames:
                        metadata[fieldname] = row[fieldname]
                else:
                    metadata = None

                if text is not None:
                    msg = models.Message.objects.create(dataset=form.instance, text=text, sender=sender, time=time, metadata=metadata)
                    msg.save()

        except Exception, e:
            print "!!!!\n"*4
            print "Exception occurred", e
            raise e

        return super(DatasetImportView, self).form_valid(form)


class DatasetExportSelectionView(LoginRequiredMixin, ProjectViewMixin, FormView):
    """ 
    View to let user select which tasks to download
    """

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


    def form_valid(self, form):
        print "form valid - self: ", self.__dict__
        print "form valid - form: ", form.__dict__
        print "form tasks:", form["tasks"].__dict__
        print "cleaned: ", form.cleaned_data["tasks"]
        print "selected tasks: ", [t.id for t in form.cleaned_data["tasks"]]

        dataset_slug = self.kwargs["dataset_slug"]
        tasks = {"tasks[]": [t.id for t in form.cleaned_data["tasks"]] }
        #print "form data: ", form_data
        print urllib.urlencode(tasks)

        return HttpResponseRedirect( "%s?%s"%(
            reverse('dataset-tasks-download', kwargs={
                "project_slug": self.get_project().slug,
                "dataset_slug": dataset_slug} ), 
            urllib.urlencode(tasks, doseq=True) ))
        #return super(DatasetExportSelectionView, self).form_valid(form)

    def get_success_url(self):
        print "get success url __dict__:", self.__dict__
        print "get success kwargs: ", self.kwargs
        print "get success form: ", self.form
        return reverse('export', kwargs={
            'project_slug': self.get_project().slug,
            'dataset_slug': self.object.slug,
        })




class DatasetExportView(LoginRequiredMixin, ProjectViewMixin, View):
    """ 
    Simple Export View 
    """

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



class DatasetTasksExportView(LoginRequiredMixin, ProjectViewMixin, View):
    """
    Task Selection View
    """

    def get(self, request, project_slug, dataset_slug, **kwargs):

        message_set = set()
        user_set = set()
        code_set = set()

        # grab the task ids from the get
        task_ids = request.GET.getlist('tasks[]')
        #print "task ids: ", task_ids
        tasks = project_models.Task.objects.filter(id__in=task_ids)

        # step through each task and find the messages, users, and codes
        for task in tasks:
            #print "task: ", task.id
            message_ids = set(task.selection.get_messages().values_list("id", flat=True))
            message_set |= message_ids

            user_ids = set([ac.id for ac in task.assigned_coders.all()])
            user_set |= user_ids

            print "scheme"

            code_objs = coding_models.Code.objects.filter(code_group__in=task.scheme.code_groups.all())
            codes = set(code_objs.values_list("id", flat=True))
            code_set |= codes

        print "message_set: ", repr(message_set)
        print "user_set: ", repr(user_set)
        print "code_set: ", repr(code_set)

        # begin a streaming response
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="%s_%s_%s.csv"'%(project_slug, dataset_slug, datetime.now().strftime("%Y%m%d-%H%M"))

        # attach a csv writer to that
        csvwriter = csv.writer(response)
        csvwriter.writerow(["id", "time", "sender", "text", "codes_str"])

        # create a utf-8 encoder
        encoder = codecs.getencoder("utf-8")

        # XXX: TODO
        # this is insanely inefficient
        message_list = sorted(message_set)
        for msg_id in message_list:

            msg_list = models.Message.objects.filter(id__exact=msg_id)
            for m in msg_list:

                # grab all instances attacahed to this 
                instances = project_models.CodeInstance.objects.filter(message=m, owner__in=user_set, code__in=code_set )
                codes_str =  u"|".join([unicode(c.code.name) for c in instances]) if instances is not None and instances.count() > 0 else ""

                # create the column values for our row
                cols = [unicode(m.id), unicode(m.time), unicode(m.sender),  unicode(m.text), codes_str]

                # encode and write them
                encoded_cols = [encoder(c)[0] for c in cols]
                csvwriter.writerow(encoded_cols)

        # return the full response
        return response


        # find our dataset & messages
        #dataset = models.Dataset.objects.filter(slug=dataset_slug)
        #messages = models.Message.objects.filter(dataset=dataset)


        return HttpResponse("yay")
