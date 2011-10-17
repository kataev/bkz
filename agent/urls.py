from django.conf.urls.defaults import *
from whs.agent.forms import *

urlpatterns = patterns('',
    url(r'^agent/(?P<id>\d*)/?$', 'whs.views.form_get',{'form':AgentForm},name='agent_get'),
    url(r'^agent/?(?P<id>\d*)/post/$', 'whs.views.form_post',{'form':AgentForm},name='agent_post'),
    url(r'^agents/store/$', 'whs.agent.views.select_store',name='agent_select_store'),

    )