# -*- coding: utf-8 -*-
from django.middleware.common import CommonMiddleware
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render

class Access(CommonMiddleware):
    def process_view(self,request,view_func, view_args, view_kwargs):
        try:
            url = resolve(request.path)
            name = url.url_name
            namespace = url.namespace
            request.namespace = namespace
#            if not request.user.has_perm('view-%s' % name):
#                response = render(request,'core/denied.html')
#                response.code_status = 504
#                return response
#            if request.method =='GET' and 'add' in name and request.user.has_perm('add_%s' % name.split('-')[0].lower()):
#                response = render(request,'core/denied.html')
#                response.code_status = 504
#                return response
#            if request.method != 'GET' and request.user.has_perm('view-%s' % name):
#                pass
        except Resolver404:
            request.namespace = None