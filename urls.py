from django.conf.urls.defaults import patterns, include, url

from django_restapi.model_resource import Collection
from django_restapi.responder import JSONResponder


from whs.bricks.models import bricks
bricks_model = Collection(
    queryset = bricks.objects.all(),
    responder = JSONResponder()
)


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'whs.main.views.main', name='main'),
    url(r'^test/$', 'whs.main.views.test', name='test'),
    url(r'^form/(?P<modelName>\w+)/(?P<id>\d+)/$', 'whs.main.views.form', name='form_id'),
    url(r'^form/(?P<modelName>\w+)/$', 'whs.main.views.form', name='form'),
    url(r'^json/bricks/(.*?)/?$', bricks_model),
    # url(r'^whs/', include('whs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
