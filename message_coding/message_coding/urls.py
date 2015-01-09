""" Default urlconf for messageCoding """

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin


# NOTE: new url segments at the top level
# should be added to the blacklist for project.Project model slugs.
urlpatterns = patterns('',

                       # Load the admin urls
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^', include('base.urls')),

)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    )