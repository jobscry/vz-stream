from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('vz_stream.views',
    (r'^stats/$', 'stream_stats', { 'month':None, 'year':None, }),
    (r'^stats/(?P<year>[0-9]{4})/$', 'stream_stats', { 'month':None, }),
    (r'^stats/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'stream_stats'),
    (r'^view/(?P<pk>[0-9]+)/$', 'view_stream'),
    (r'^view/$', 'view_stream', { 'pk':None }),
    (r'^update/(?P<pk>[0-9]+)/$', 'update'),
    (r'^update/$', 'update', { 'pk':None }),
)
