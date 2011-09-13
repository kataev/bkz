from django.conf.urls.defaults import *
from whs.agent.forms import *

urlpatterns = patterns('whs.views',
    url(r'^agent/(?P<id>\d*)/?$', 'form_get',{'form':AgentForm},name='agent_get'),
    url(r'^agent/?(?P<id>\d*)/post/$', 'form_post',{'form':AgentForm},name='agent_post'),
    )