# -*- coding: utf-8 -*-
import re
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.template import loader, Context

import trml2pdf
from pytils.numeral import rubles

# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' +\
                 u'|' +\
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' %\
                 (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                  unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                  unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))

def pdf_render_to_response(template, context, filename=None, prompt=False):
    response = HttpResponse(mimetype='application/pdf')
    if not filename:
        filename = template+'.pdf'
    cd = []
    if prompt:
        cd.append('attachment')
    cd.append('filename=%s' % filename)
    response['Content-Disposition'] = '; '.join(cd)
    tpl = loader.get_template(template)
    tc = {'filename': filename}
    tc.update(context)
    ctx = Context(tc)

    x = tpl.render(ctx)
    x = re.sub(RE_XML_ILLEGAL, "?", x)

    pdf = trml2pdf.parseString(x.encode("utf-8"))
    response.write(pdf)
    return response


class BillMixin(object):
    def opers(self):
        opers = list(self.solds.all()) + list(self.pallets.all())
        for o in opers:
            o.doc = self
        return opers

    @property
    def tara_return(self):
        return self.date + relativedelta(months=+1)

    @property
    def total(self):
        return sum([s.amount for s in self.solds.all()])

    @property
    def netto(self):
        return sum([x.netto for x in self.opers])

    @property
    def brutto(self):
        return sum([x.brutto for x in self.opers])

    @property
    def tara(self):
        return sum([getattr(x,'tara',0) for x in self.opers])

    @property
    def items(self):
        return sum([x.items for x in self.opers()])

    @property
    def money(self):
        return sum([x.money for x in self.opers()])

    @property
    def nds(self):
        return sum([x.nds for x in self.opers()])

    @property
    def in_total(self):
        return sum([x.in_total for x in self.opers()])

    @property
    def pages(self):
        return int(len(self.opers())/6 + 1)

    @property
    def rubles(self):
        rub = rubles(self.in_total)
        if len(rub) < 62:
            return dict(f=rub,)
        else:
            r = rub.split(' ')
            f = reduce(lambda m,s: m+u' %s' %s,r[:len(r)/2])
            s = reduce(lambda m,s: m+u' %s' % s,r[len(r)/2:])
            return dict(f=f,s=s)

class PalletMixin(object):
    @property
    def nomenclature(self):
        return dict(title=u'Поддоны - Возвратная тара',intcode=131)

    @property
    def netto(self):
        return 0

    @property
    def brutto(self):
        return 0

#    @property
#    def price(self):
#        return 200.00

    @property
    def money(self):
        return self.amount * self.price

    @property
    def items(self):
        return self.amount

    @property
    def nds(self):
        return 0

    @property
    def in_total(self):
        return self.money

class OperationsMixin(object):
    @property
    def nomenclature(self):
        return self.brick.nomenclature

    @property
    def money(self):
        return self.amount * self.price

    @property
    def netto(self):
        return int(round(self.amount * self.brick.mass))

    @property
    def brutto(self):
        return self.netto + 20 * self.tara

    @property
    def okei(self):
        return 796

    @property
    def package(self):
        return u'поддон'

    @property
    def space(self):
        return 288

    @property
    def items(self):
        return self.space * self.tara

    @property
    def nds(self):
        return round(self.doc.seller.nds * self.money,2)

    @property
    def get_nds_display(self):
        nds = self.doc.seller.nds
        if nds == 0:
            return u'б/НДС'
        else:
            return str(float(nds))[2:]

    @property
    def in_total(self):
        return self.money + self.nds