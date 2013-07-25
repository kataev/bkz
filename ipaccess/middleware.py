# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from bkz.ipaccess.models import IPAccess


class IPAccessMiddleware(object):
    def process_request(self, request):
        if request.user == AnonymousUser():
            remoteip = request.META['REMOTE_ADDR']
            try:
                ipaccess = IPAccess.objects.get(ip=remoteip)
                request.user = ipaccess.user
            except IPAccess.DoesNotExist:
                pass
        return None
