# -*- coding: utf-8 -*-
import re
import datetime

from django.db import models

from bkz.utils import UrlMixin, ru_date
from bkz.whs.constants import cavitation_c, color_c, get_name, css_dict

tto_regexp = re.compile(r'(\d+)+')


class Forming(models.Model, UrlMixin):
    """
    Хранит в себе информацию о формовании продукции. Отражается на журнал оператора пресса.
    """
    date = models.DateField(u'Дата', default=datetime.date.today())
    cavitation = models.PositiveIntegerField(u"Пустотность", choices=cavitation_c, default=cavitation_c[0][0])
    width = models.ForeignKey('whs.Width', verbose_name=u'Размер', default=1)
    color = models.IntegerField(u'Цвет', choices=color_c, default=color_c[0][0])

    tts = models.IntegerField(u'№ ТТС')
    density = models.FloatField(u'Плот.')
    vacuum = models.FloatField(u'Вак.')
    empty = models.BooleanField('Пуст.', default=False)

    order = models.IntegerField(u'Порядок', default=0)

    get_name = property(get_name)

    def __unicode__(self):
        if self.pk:
            return u'Формовка %s от %s на телегу № %d' % (self.get_name, self.date, self.tts)
        else:
            return u'Новая формовка'

    @property
    def amount(self):
        return self.width.tts


    @property
    def lab(self):
        return list(self.half.all()) + list(self.raw.all()) + list(self.bar.all())

    @property
    def css(self):
        return css_dict['color'].get(self.color, 'None')

    class Meta:
        verbose_name = u'Формовка'
        verbose_name_plural = u'Формовка'
        unique_together = ('date', 'tts')
        ordering = ('-date', 'order')


class Warren(models.Model, UrlMixin):
    """
    Хранит в себе информацию о садке продукции с сушильных телег на обжиговые телеги. Отражается на журнал оператора садочного коплекса
    """
    date = models.DateField(u'Дата', null=True, blank=True)

    tts = models.IntegerField(u'ТТС')
    tto = models.CharField(u'ТТО', null=True, blank=True, max_length=5)
    add = models.IntegerField(u'Кол-во', null=True, blank=True)

    brocken = models.CharField(u'Брак', null=True,blank=True, max_length=10)
    cause = models.ManyToManyField('lab.Cause', verbose_name=u'Прич. брака', null=True, blank=True,
                                   limit_choices_to={'type': 'warren'})

    source = models.ForeignKey('self', verbose_name=u'ТТС', related_name='consumer', null=True, blank=True)
    forming = models.OneToOneField(Forming, verbose_name=u'Формовка', null=True, blank=True)
    part = models.ForeignKey('lab.Part', verbose_name=u'Партия', null=True, blank=True, related_name='warrens',
                             limit_choices_to={'pk': 1})

    order = models.IntegerField(u'Порядок', default=0)

    def __unicode__(self):
        if self.pk:
            return u'Укладка от %s, c ТТC № %s' % (self.date, self.tts)
        else:
            return u'Новая укладка'

    @property
    def get_tto(self):
        return map(int, tto_regexp.findall(self.tto))

    @property
    def pie(self):
        if self.tto:
            queryset = self.consumer.all()
            return [ (round(1./len(queryset),2),w.tts) for w in queryset ]
        else:
            if self.brocken:
                if u'%' in self.brocken:
                    n, = self.brocken.split('%')
                    return n/100.
                elif u'п' in self.brocken:
                    return 1
                else:
                    return 1

    class Meta:
        ordering = ('-date', 'order')
        verbose_name = u'Укладка'
        verbose_name_plural = u'Укладка'
        unique_together = ('date', 'tts')