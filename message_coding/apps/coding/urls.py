"""urlconf for the coding application"""

from django.conf.urls import url, patterns

import views

urlpatterns = patterns('',
                       url(r'^(?P<scheme_pk>[\d]+)/$',
                           views.SchemeEditorView.as_view(),
                           name='scheme'),
                       )
