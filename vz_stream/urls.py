from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('vz_stream.views',
    (r'^update/(?P<pk>[0-9]+)/$', 'update'),
    (r'^update/$', 'update', { 'pk':None }),
)
