from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import message_coding.apps.coding.models as coding_models
import message_coding.apps.dataset.models as dataset_models
import message_coding.apps.project.models as project_models
from django.db import transaction
import traceback
import sys
import path
from time import time
from django.conf import settings
import json

class Command(BaseCommand):
    """
    Import test coding data into the database.

    .. code-block :: bash

        $ python manage.py import_test_coding_data <code_file_path> <code_instance_file_path> <tweets_file_path>

    """
    args = '<code_file_path> <code_instance_file_path> <tweets_file_path>'
    help = "Import test coding data into the database."
    option_list = BaseCommand.option_list + (
        make_option('-d', '--dataset',
                    action='store',
                    dest='dataset',
                    help='Set a target dataset to add to'
        ),
    )

    def handle(self, code_file, code_instance_file, tweet_file, **options):

        dataset = options.get('dataset', None)
        if not dataset:
            dataset = code_file + '|' + code_instance_file + '|' + tweet_file

        for f in [code_file, code_instance_file, tweet_file]:
            if not path.path(f).exists():
                raise CommandError("Filename %s does not exist" % f)

        start = time()
        dataset_obj, created = dataset_models.Dataset.objects.get_or_create(name=dataset, description=dataset)
        if created:
            print "Created dataset '%s' (%d)" % (dataset_obj.name, dataset_obj.id)
        else:
            print "Adding to existing dataset '%s' (%d)" % (dataset_obj.name, dataset_obj.id)


        codes = []
        code_instances = []
        tweets = []

        with open(code_file, 'rb') as fp:
            code_file_str = fp.read()
            codes = json.loads(code_file_str)

        with open(code_instance_file, 'rb') as fp:
            code_instance_str = fp.read()
            code_instances = json.loads(code_instance_str)

        with open(tweet_file, 'rb') as fp:
            tweet_file_str = fp.read()
            tweets = json.loads(tweet_file_str)

        importer = Importer(dataset_obj, codes, code_instances, tweets)
        importer.run()


        
        print "Time: %.2fs" % (time() - start)


class Importer(object):
    commit_every = 100
    print_every = 1000

    def __init__(self, dataset, codes, code_instances, tweets):
        self.dataset = dataset
        self.codes = codes
        self.code_instances = code_instances
        self.tweets = tweets
        self.line = 0
        self.imported = 0
        self.not_tweets = 0
        self.errors = 0


    def _import_codes(self, codes):
        with transaction.atomic(savepoint=False):
            for code in codes:
                try:
                    code = create_an_instance_from_json(json_str, self.dataset)
                    if message:
                        self.imported += 1


                    else:
                        self.not_tweets += 1
                except:
                    self.errors += 1
                    print >> sys.stderr, "Import error on line %d" % self.line
                    traceback.print_exc()

        if settings.DEBUG:
            # prevent memory leaks
            from django.db import connection
            connection.queries = []


    def run(self):
        transaction_group = []

        start = time()

        for json_str in self.fp:
            self.line += 1
            json_str = json_str.strip()
            transaction_group.append(json_str)

            if len(transaction_group) >= self.commit_every:
                self._import_group(transaction_group)
                transaction_group = []

            if self.line > 0 and self.line % self.print_every == 0:
                print "%6.2fs | Reached line %d. Imported: %d; Non-tweets: %d; Errors: %d" % (
                time() - start, self.line, self.imported, self.not_tweets, self.errors)

        if len(transaction_group) >= 0:
            self._import_group(transaction_group)

        print "%6.2fs | Finished %d lines. Imported: %d; Non-tweets: %d; Errors: %d" % (
        time() - start, self.line, self.imported, self.not_tweets, self.errors)

    def _init_project(self):
        admin = settings.AUTH_USER_MODEL.objects.get(id=1)
        project = project_models.Project(owner=admin, name='test code', description='test code')
        project.save()

        self.admin = admin
        self.project = project
        self.scheme_code_groups = {}
        self.scheme_tasks = {}

    def _get_or_create_scheme(self, scheme_id):
        scheme, created = coding_models.Scheme.objects.get_or_create(project=self.project,
                                                                     name='scheme ' + scheme_id,
                                                                     owner=self.admin)
        if created:
            code_group = coding_models.CodeGroup(name='scheme ' + scheme_id + ' code group',
                                                 description= 'scheme ' + scheme_id + 'test code group',
                                                 scheme=scheme)
            code_group.save()
            self.scheme_code_groups[scheme_id] = code_group

            task = project_models.task(owner=self.admin, project=self.project, scheme=scheme)
            task.save()
            self.scheme_taskss[scheme_id] = task

        return self.scheme_code_groups[scheme_id]

    def _import_a_code(self, code):
        code_group = self._get_or_create_scheme(scheme_id=code.scheme_id)
        code_obj = coding_models.Code(name=code.name, description=code.description, code_group=code_group)
        code_obj.save()

