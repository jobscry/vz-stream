from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('vz_stream.views',
    (r'^view/(?P<pk>[0-9]+)/$', 'view_stream'),
    url(r'^view/$', 'view_stream', { 'pk':None }, "vz_stream:stream_view"),
    (r'^update/(?P<pk>[0-9]+)/$', 'update'),
    (r'^update/$', 'update', { 'pk':None }),
)
