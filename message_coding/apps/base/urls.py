"""urlconf for the base application"""

from django.conf.urls import url, patterns, include

from message_coding.apps.base import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       url(r'^home/$', views.UserDashboard.as_view(), name='user_dash'),
                       url(r'^accounts/', include('django.contrib.auth.urls')),

                       # REST Api urls
                       url(r'^api/', include('apps.api.urls')),

                       # Project urls
                       url(r'^', include('apps.project.urls')),

)
