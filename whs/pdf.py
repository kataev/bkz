# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from pytils.numeral import rubles


class BillMixin(object):
    @property
    def opers(self):
        opers = list(self.solds.all()) + list(self.pallets.all())
        for o in opers:
            o.doc = self
        return opers

    @property
    def tara_return(self):
        return self.date + relativedelta(months=+1)

    @property
    def amount(self):
        return sum([s.amount for s in self.solds.all()], 0)

    @property
    def netto(self):
        return sum([x.netto for x in self.opers], 0)

    @property
    def brutto(self):
        return sum([x.brutto for x in self.opers], 0)

    @property
    def tara(self):
        return sum([s.tara for s in self.solds.all()], 0)

    @property
    def items(self):
        return sum([x.items for x in self.opers], 0)

    @property
    def money(self):
        return sum([x.money for x in self.opers], 0)

    @property
    def nds(self):
        return sum([x.nds for x in self.opers], 0)

    @property
    def in_total(self):
        return sum([x.in_total for x in self.opers], 0)

    @property
    def pages(self):
        return 1000

    @property
    def rubles(self):
        return rubles(self.in_total)


class PalletMixin(object):
    @property
    def nomenclature(self):
        return dict(title=u'Поддоны - Возвратная тара', intcode=131)

    @property
    def netto(self):
        return 0

    @property
    def brutto(self):
        return 0

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


class SoldMixin(object):
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
        return round(self.doc.seller.nds * self.money, 2)

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
