# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class IPAccess(models.Model):
    ip = models.IPAddressField(unique=True, db_index=True)
    user = models.ForeignKey(User, verbose_name='user that authenticates')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'IP Access'
        verbose_name_plural = 'IP Accesses'

    class Admin:
        list_display = ('ip', 'user')