# -*- coding: utf-8 -*-
from django.middleware.common import CommonMiddleware
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render


class Access(CommonMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            url = resolve(request.path)
            name = url.url_name
            namespace = url.namespace
            request.namespace = namespace
            if '-' in name:
                model, action = name.lower().split('-')
                if action == 'list' or action == 'print':
                    action = 'view'
                if action == 'view' and request.user.has_perm('%s.%s_%s' % (namespace, 'change', model)):
                    action = 'change'
                if not request.user.has_perm('%s.%s_%s' % (namespace, action, model)):
                    response = render(request, 'core/denied.html')
                    response.code_status = 504
                    return response
        except Resolver404:
            request.namespace = None
