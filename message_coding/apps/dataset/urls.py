"""urlconf for the dataset application"""

from django.conf.urls import url, patterns

import views

urlpatterns = patterns('',

   url(r'^import/$',
       views.DatasetImportView.as_view(),
       name='dataset_import'),

   url(r'^(?P<dataset_slug>[\w-]+)/$',
       views.DatasetDetailView.as_view(),
       name='dataset'),

   url(r'^export/(?P<dataset_slug>[\w-]+)/$',
        views.DatasetExportSelectionView.as_view(),
        name='dataset-export'),

   url(r'^download/(?P<dataset_slug>[\w-]+)/$',
        views.DatasetExportView.as_view(),
        name='dataset-download'),

    url(r'^download-tasks/(?P<dataset_slug>[\w-]+)/$',
        views.DatasetTasksExportView.as_view(),
        name='dataset-tasks-download'),


)
