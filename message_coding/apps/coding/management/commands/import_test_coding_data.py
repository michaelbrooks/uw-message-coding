from optparse import make_option
import traceback
import sys
from time import time
import json
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
import path
import re

import message_coding.apps.coding.models as coding_models
import message_coding.apps.dataset.models as dataset_models
import message_coding.apps.project.models as project_models


User = get_user_model()

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class AttrDict(dict):
    _getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

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
        created_at = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        if not dataset:
            dataset = "dataset-" + created_at

        for f in [code_file, code_instance_file, tweet_file]:
            if not path.path(f).exists():
                raise CommandError("Filename %s does not exist" % f)

        start = time()
        dataset_obj, created = dataset_models.Dataset.objects.get_or_create(name=dataset,
                                                                            defaults={
                                                                                "description":dataset,
                                                                                "owner": User.objects.get(id=1),
                                                                                "created_at": created_at,
                                                                                "slug": "dataset-" + str(created_at),
                                                                            })
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
            codes = map(lambda x: AttrDict(x), codes)

        with open(code_instance_file, 'rb') as fp:
            code_instance_str = fp.read()
            code_instances = json.loads(code_instance_str)
            code_instances = map(lambda x: AttrDict(x), code_instances)

        with open(tweet_file, 'rb') as fp:
            tweet_file_str = fp.read()
            tweets = json.loads(tweet_file_str)
            tweets = map(lambda x: AttrDict(x), tweets)

        importer = Importer(dataset_obj, codes, code_instances, tweets)
        importer.run()


        
        print "Time: %.2fs" % (time() - start)


class Importer(object):
    commit_every = 10
    print_every = 10

    def __init__(self, dataset, codes, code_instances, tweets):
        self.dataset = dataset
        self.codes = codes
        self.code_instances = code_instances
        self.tweets = tweets
        self.line = 0
        self.imported = 0
        self.not_code_instances = 0
        self.errors = 0




    def run(self):
        self._init_project()
        self.run_import_codes()
        self.run_import_tweets()
        self.run_import_code_instances()


    def _init_project(self):
        admin = User.objects.get(id=1)
        created_at = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
        project = project_models.Project(owner=admin, name='test code', description='test code', slug="dataset-" + str(created_at))
        project.save()
        project.members.add(admin)
        project.save()

        self.admin = admin
        self.project = project
        self.scheme_code_groups = {}
        self.scheme_tasks = {}
        self.scheme_mapping = {}
        #self.scheme_mapping_inverse = {}
        self.code_mapping = {}

    def _get_or_create_scheme_code_group(self, scheme_id):
        if self.scheme_mapping.get(scheme_id) is None:
            scheme = coding_models.Scheme(project=self.project,
                                          name='scheme ' +  str(scheme_id),
                                          owner=self.admin)
            scheme.save()
            self.scheme_mapping[scheme_id] = scheme
            #self.scheme_mapping_inverse[scheme.id] = scheme_id

            code_group = coding_models.CodeGroup(name='scheme ' + str(scheme_id) + ' code group',
                                                 description= 'scheme ' + str(scheme_id) + 'test code group',
                                                 scheme=scheme)
            code_group.save()

            self.scheme_code_groups[scheme.id] = code_group
            task = project_models.Task(name="task" + str(scheme_id),
                                       owner=self.admin, project=self.project, scheme=scheme)
            task.save()

            self.scheme_tasks[scheme.id] = task
        #import pdb
        #pdb.set_trace()
        return self.scheme_code_groups[self.scheme_mapping[scheme_id].id]

    def _import_a_code(self, code):
        print code
        code_group = self._get_or_create_scheme_code_group(scheme_id=code.scheme_id)
        code_obj = coding_models.Code(name=code.name, description=code.description, code_group=code_group)
        code_obj.save()
        self.code_mapping[code.id] = code_obj
        return code_obj
    
    def _import_codes(self, codes):
        with transaction.atomic(savepoint=False):
            for code in codes:
                #try:
                #import pdb
                #pdb.set_trace()
                code = self._import_a_code(code)

                    #if code:
                    #    self.imported += 1
                    #else:
                       # self.not_code_instances += 1
                #except:
                    #self.errors += 1
                    #print >> sys.stderr, "Import error on line %d" % self.line
                    #traceback.print_exc()

    
    def run_import_codes(self):
        transaction_group = []

        #start = time()

        for code in self.codes:
            #self.line += 1
            transaction_group.append(code)

            if len(transaction_group) >= self.commit_every:
                self._import_codes(transaction_group)
                transaction_group = []

            #if self.line > 0 and self.line % self.print_every == 0:
            #    print "%6.2fs | Reached line %d. Imported: %d; Non-tweets: %d; Errors: %d" % (
            #    time() - start, self.line, self.imported, self.not_code_instances, self.errors)

        if len(transaction_group) >= 0:
            self._import_codes(transaction_group)

        #print "%6.2fs | Finished %d lines. Imported: %d; Non-tweets: %d; Errors: %d" % (
        #time() - start, self.line, self.imported, self.not_code_instances, self.errors)

    def _import_a_tweet(self, tweet):

        tweet_obj = dataset_models.Message(id=tweet.id,
                                           dataset=self.dataset,
                                           sender=tweet.screen_name,
                                           time=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                                           text=striphtml(tweet.embed_code))
        tweet_obj.save()
        return tweet_obj

    def _import_tweets(self, tweets):
        with transaction.atomic(savepoint=False):
            for tweet in tweets:
                try:
                    code = self._import_a_tweet(tweet)
                except:
                    traceback.print_exc()


    def run_import_tweets(self):
        transaction_group = []


        for tweet in self.tweets:
            transaction_group.append(tweet)

            if len(transaction_group) >= self.commit_every:
                self._import_tweets(transaction_group)
                transaction_group = []

        if len(transaction_group) >= 0:
            self._import_tweets(transaction_group)


    def _import_a_code_instance(self, code_instance):
        task_assigner, created = User.objects.get_or_create(id=code_instance.assignment_id,
                                                                                defaults={
                                                                                    "password": make_password('user' + str(code_instance.assignment_id)),
                                                                                    "is_superuser": False,
                                                                                    "username": 'user' + str(code_instance.assignment_id),
                                                                                    "first_name": 'user',
                                                                                    "last_name": code_instance.assignment_id,
                                                                                    "is_staff": False,
                                                                                    "is_active": True,
                                                                                    "date_joined": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

                                                                                })


        code = self.code_mapping[code_instance.code_id]

        tweet = dataset_models.Message.objects.get(id=code_instance.tweet_id)
        task = self.scheme_tasks[code.code_group.scheme.id]

        self.project.members.add(task_assigner)
        self.project.save()

        code_instance_obj = project_models.CodeInstance(created_at=code_instance.date,
                                        message=tweet,
                                        code=code,
                                        owner=task_assigner,
                                        task=task)

        code_instance_obj.save()
        return code_instance_obj

    def _import_code_instances(self, code_instances):
        with transaction.atomic(savepoint=False):
            for code_instance in code_instances:
                try:
                    #print code_instance
                    code_instance = self._import_a_code_instance(code_instance)
                    if code_instance:
                        self.imported += 1
                    else:
                        self.not_code_instances += 1

                except:
                    self.errors += 1
                    print >> sys.stderr, "Import error on line %d" % self.line
                    traceback.print_exc()



    def run_import_code_instances(self):
        transaction_group = []
        
        start = time()
        
        for code_instance in self.code_instances:
            self.line += 1
            transaction_group.append(code_instance)

            if len(transaction_group) >= self.commit_every:
                self._import_code_instances(transaction_group)
                transaction_group = []
                
            if self.line > 0 and self.line % self.print_every == 0:
                print "%6.2fs | Reached line %d. Imported: %d; Non-tweets: %d; Errors: %d" % (
                time() - start, self.line, self.imported, self.not_code_instances, self.errors)    

        if len(transaction_group) >= 0:
            self._import_code_instances(transaction_group)        
                
 
        print "%6.2fs | Finished %d lines. Imported: %d; Non-tweets: %d; Errors: %d" % (
        time() - start, self.line, self.imported, self.not_code_instances, self.errors)    
