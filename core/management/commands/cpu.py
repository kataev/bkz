# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from bkz.cpu.relsib import lrc,termodat,lrc_old,parse_data
import psycopg2

class Command(BaseCommand):
    help = "Commands for lagasy db"
    def handle(self, *args, **options):
        self.relsib_test()

    def relsib_test(self):
    	con = psycopg2.connect(user='bteam', host='', database='bteam', password='bteam',port='5433')
    	cur = con.cursor()
    
    	m = termodat(1, 0, 24)

    	print m + lrc_old(m) == '010300000018e4'

    	data = parse_data('01F80226025F028A01B201D60000FFFF001A19461C6E1F7521C4249B2629262E24EC01B4121A14517D001F521ABB150E',4)

    	print data == [50.4, 55.0, 60.7, 65.0, 43.4, 47.0, 0, 0.1, 2.6, 647.0, 727.8, 805.3, 864.4, 937.1, 976.9, 977.4, 945.2, 43.6, 463.4, 520.1, 0, 801.8, 684.3, 539.0]

    	for r,value in enumerate(data):
    		print r,value
    		cur.execute('INSERT INTO cpu_value (datetime,code,field,value) VALUES (NOW(),%d, %s, %f);' % (1, r+1, value) )
