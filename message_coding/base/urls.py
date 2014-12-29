"""urlconf for the base application"""

from django.conf.urls import url, patterns, include


urlpatterns = patterns('base.views',
                       url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('',
                        url(r'^accounts/', include('django.contrib.auth.urls')),
                        # url(r'^login/$', 'django.contrib.auth.views.login'),
                        # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
