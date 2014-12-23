"""urlconf for the projects application"""

from django.conf.urls import url, patterns

import views

urlpatterns = patterns('apps.dataset.views',

                    # All project-related-urls should start with the project code: ^(?P<project_pk>\d+)/
                       url(r'^(?P<pk>\d+)/$',
                           views.DatasetDetailView.as_view(),
                           name='dataset'),

                       
)
