"""urlconf for the projects application"""

from django.conf.urls import url, patterns

import views

urlpatterns = patterns('',

                       url(r'^import/$',
                           views.DatasetImportView.as_view(),
                           name='dataset_import'),

                       url(r'^(?P<dataset_slug>[\w-]+)/$',
                           views.DatasetDetailView.as_view(),
                           name='dataset'),

)
