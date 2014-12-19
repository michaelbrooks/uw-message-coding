"""urlconf for the base application"""

from django.conf.urls import url, patterns
from django.contrib.auth.views import login


urlpatterns = patterns('base.views',
    url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('', 
	(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)