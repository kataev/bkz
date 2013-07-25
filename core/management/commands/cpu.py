# -*- coding: utf-8 -*-
import psycopg2

from django.core.management.base import BaseCommand
from BeautifulSoup import BeautifulStoneSoup

from bkz.cpu.relsib import lrc, termodat, parse_data
from itertools import *
from collections import Counter


class Command(BaseCommand):
    help = "Commands for lagasy db"

    def handle(self, *args, **options):
        #self.relsib_test()
        self.svg()


    def relsib_test(self):
        con = psycopg2.connect(user='bteam', host='', database='bteam', password='bteam', port='5433')
        cur = con.cursor()

        m = termodat(1, 0, 24)

        print m + lrc_old(m) == '010300000018e4'

        data = parse_data(
            '01F80226025F028A01B201D60000FFFF001A19461C6E1F7521C4249B2629262E24EC01B4121A14517D001F521ABB150E', 4)

        print data == [50.4, 55.0, 60.7, 65.0, 43.4, 47.0, 0, 0.1, 2.6, 647.0, 727.8, 805.3, 864.4, 937.1, 976.9, 977.4,
                       945.2, 43.6, 463.4, 520.1, 0, 801.8, 684.3, 539.0]

        for r, value in enumerate(data):
            print r, value
            cur.execute(
                'INSERT INTO cpu_value (datetime,code,field,value) VALUES (NOW(),%d, %s, %f);' % (1, r + 1, value))


    def svg(self):
        xml = ''.join(l for l in file('/home/bteam/Dropbox/mm/bkz/striped.svg').readlines())
        soup = BeautifulStoneSoup(xml, selfClosingTags=[u'polygon', u'polyline', u'path', u'line', u'rect'])
        # for name in [u'polygon',  u'polyline', u'text', u'path', u'line', u'rect']:
        tags = soup.findAll()
        # print name.upper()
        css = {'text': 'color:#000;fill:'}
        for k, g in groupby(sorted(chain.from_iterable(t.attrs for t in tags)), key=lambda x: str(x[0])):
            if 'y' not in k and 'x' not in k and k not in ('d', 'transform', 'points'):
                c = Counter(v for k, v in g)
                i = 0
                for ke, v in c.items():
                    i += 1
                    if v > 10:
                        style = u'%s:%s' % (k, ke)
                        css[u'.%s%d' % (k[:3] + k[-3:], i)] = style
                        for j, t in enumerate(soup.findAll(attrs={k: ke})):
                            del t[k]
                            t['class'] = t.get('class', u'') + u' %s%d' % (k[:3] + k[-3:], i)

        for t in soup.findAll('text'):
            t['fill'] = '#000'
        new = file('bkz.html', 'w')
        style = unicode(u'\n'.join(u'%s {%s}' % (k, v) for k, v in css.items()))
        new.write('<html> <head> <title>BKZ</title> <style>')
        new.write(style)
        new.write('</style> </head> <body>')
        new.write(soup.prettify())
        new.write('</body> </html>')
        new.close()
