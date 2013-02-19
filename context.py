# -*- coding: utf-8 -*-
from bkz.whs.models import Brick
from django.contrib import messages

def bricks(request):
    if getattr(request,'namespace',None) == 'whs':
        Bricks = Brick.objects.all()
        return dict(Bricks=Bricks)
    return {}

nav = dict(
    main= (
        ('whs:Brick-list', 'icon-align-justify', u'Склад'),
        ('lab:index', 'icon-fullscreen', u'Лаборатория'),
        ('make:index', 'icon-tasks', u'Производство'),
        ('energy:index', 'icon-energy', u'Энергоресурсы'),
        ('it:index', 'icon-hdd', u'ИТ'),
        ('price', 'icon-shopping-cart', u'Прайс'),
    ),
    whs=(
        ('whs:Brick-list', 'icon-align-justify', u'Склад'),
        ('divider',),
        ('whs:Bill-list', 'icon-whs', u'Реализация'),
        ('whs:Add-list', 'icon-man', u'Производство'),
        ('whs:Sorting-list', 'icon-indent-right', u'Сортировка'),
        ('whs:Agent-list', 'icon-Agent', u'Контрагенты'),
        ),
    it=(
        ('it:index', 'icon-hdd', u'ИТ'),
        ),
    energy=(
        ('energy:index', 'icon-energy', u'Показания'),
        ('energy:energy', 'icon-magnet', u'Энергоресурсы'),
        ('energy:teplo', 'icon-wrench', u'Тепло'),
        ),
    lab = (
        ('lab:index',' icon-fullscreen', u'Лаборатория'),
        ('lab:journal',' icon-book', u'Журнал'),
        ('lab:stats',' icon-signal', u'Характеристики'),
    ),
    make = (
        ('make:cpu:index','icon-fire',u'ЦПУ'),
        ('make:index','icon-align-justify',u'Производство'),
        ('make:forming', 'icon-filter', u'Формовка'),
        ('make:warren', 'icon-resize-full', u'Укладка'),
        )
)
menu = dict(
    energy=(
        ('energy:Energy-add', 'icon-Energy', u'Энергоресурсы'),
        ('energy:Teplo-add', 'icon-Teplo', u'Тепло'),
        ),
    it=(
        ('it:Device-add', 'icon-inbox', u'Устройство или картридж'),
        ('it:Buy-add', 'icon-tint', u'Накладную'),
        ('it:Plug-add', 'icon-adjust', u'Замену'),
        ),
    whs=(
        ('whs:Bill-add', 'icon-Bill', u'Накладную'),
        ('whs:Sorting-add', 'icon-Sorting', u'Сортировку'),
#        ('whs:Inventory-add', 'icon-Inventory', u'Инвентаризацию'),
        ('divider',),
        ('whs:Brick-add', 'icon-Brick', u'Кирпич'),
        ('whs:Agent-add', 'icon-Agent', u'Контрагента'),
        ),
    lab = (
        ('lab:Batch-add','',u'Партия'),
        ('divider',),
        ('lab:WaterAbsorption-add','',u'Водопоглощение'),
        ('lab:Efflorescence-add','',u'Высолы'),
        ('lab:FrostResistance-add','',u'Морозостойкость'),
        ('lab:SEONR-add','',u'Уд.эф.акт.ест.рад.'),
        ('lab:HeatConduction-add','',u'Теплопроводность'),
        ('lab:Cause-add','',u'Дефект'),
    ),
    make = (
        ('make:Forming-add','',u'Формовку'),
        ('make:Warren-add','',u'Укладку'),
        ('lab:Cause-add','',u'Дефект'),  
        ),
)

from django.core.urlresolvers import reverse,NoReverseMatch
def test_urls(urls):
    for d in urls.values():
        for url in d:
            if len(url) > 1:
                try:
                    reverse(url[0])
                except NoReverseMatch:
                    raise NoReverseMatch(url)
test_urls(nav)
test_urls(menu)

def namespace(request):
    namespace = getattr(request,'namespace',None) or 'main'
    return dict(nav=nav.get(namespace), menu=menu.get(namespace),current_app=namespace)


def flash(request):
    levels = [m.level for m in messages.get_messages(request)]
    if any(l == 40 for l in levels): return {'level':'error'}
    if any(l == 30 for l in levels): return {'level':'warning'}
    if all(l == 25 for l in levels) and levels: return {'level':'success'}
    if any(l == 20 for l in levels): return {'level':'info'}
    return {}
