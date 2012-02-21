from django.conf.urls.defaults import *
from whs.agent.forms import *

urlpatterns = patterns('',
    url(r'^agent/(?P<id>\d*)/?$', 'whs.views.flat_form', {'Form':AgentForm}, name='agent'),
    url(r'^agents$', 'whs.agent.views.agents', name='agents'),
)