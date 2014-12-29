""" Default urlconf for messageCoding """

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin


urlpatterns = patterns('',

                       # Examples:
                       # url(r'^$', 'messageCoding.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^user_dash/', 'apps.project.views.index'),

                       # Load the admin urls
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^', include('base.urls')),

                       # Project urls
                       url(r'^', include('apps.project.urls')),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )