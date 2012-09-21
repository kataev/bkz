# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import logging

from suds.client import Client

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

class Command(BaseCommand):
    help = "Connect to 1c web service"
    def handle(self, label, *args, **options):
        if label == 'get_agent':
            self.get_agent(*args[:3])
        else:
            raise CommandError(u'Select operation')

    def get_agent(self,username,password,url='http://sk/ws/ws1.1cws?wsdl'):
        client = Client(url,username=username, password=password)
        print unicode(client)
        print client.service.get_agent('000000347')