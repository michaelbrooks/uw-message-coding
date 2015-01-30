"""urlconf for the projects application"""

from django.conf.urls import url, patterns, include

import views

task_urls = patterns('',
                        url(r'^$',
                            views.TaskDetailView.as_view(),
                            name='task'),

                        url(r'edit/$',
                            views.EditTaskView.as_view(),
                            name='task_edit'),

                        url(r'^code/$',
                            views.CodingView.as_view(),
                            name='coding'),

                        url(r'^code/(?P<page>\d+)/$',
                            views.CodingView.as_view(),
                            name='coding_page'),
)

project_slug_urls = patterns('',
                             url(r'^tasks/(?P<task_pk>\d+)/',
                                 include(task_urls)),

                             url(r'^datasets/',
                                 include('apps.dataset.urls')),

                             url(r'^$',
                                 views.ProjectDetailView.as_view(),
                                 name='project'),
)

urlpatterns = patterns('apps.project.views',
                       url(r'^project/create/$',
                           views.CreateProjectView.as_view(),
                           name='project_create'),
                       url(r'^(?P<project_slug>[\w-]+)/edit/$',
                            views.UpdateProjectView.as_view(),
                            name="project_update"),

                       url(r'^(?P<project_slug>[\w-]+)/', include(project_slug_urls)),

)
