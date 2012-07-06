# -*- coding: utf-8 -*-
from django.middleware.common import CommonMiddleware
from django.core.urlresolvers import resolve, Resolver404

class Access(CommonMiddleware):
    def process_view(self,request,view_func, view_args, view_kwargs):
        try:
            namespace = resolve(request.path).namespace
            request.namespace = namespace
        except Resolver404:
            request.namespace = ''
