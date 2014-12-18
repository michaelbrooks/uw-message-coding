"""urlconf for the projects application"""

from django.conf.urls import url, patterns

import views

urlpatterns = patterns('apps.project.views',

                    # All project-related-urls should start with the project code: ^(?P<project_pk>\d+)/
                       url(r'^(?P<pk>\d+)/$',
                           views.ProjectDetailView.as_view(),
                           name='project'),

		       url(r'^create/$', 
			   views.CreateProjectView.as_view(),
			   name='project_create'),
                       
                       url(r'^(?P<project_pk>\d+)/task/(?P<pk>\d+)/$',
                           views.TaskDetailView.as_view(),
                           name='project_task'),

                       url(r'^(?P<project_pk>\d+)/task/create/$',
                           views.CreateTaskView.as_view(),
                           name='project_task_create'),
)
