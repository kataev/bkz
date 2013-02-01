# -*- coding: utf-8 -*-
from bkz.whs.models import Brick

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
#        ('energy:index', 'icon-energy', u'Энергоресурсы'),
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
        ('energy:index', 'icon-energy', u'Энергоресурсы'),
        ),
    lab = (
        ('lab:index',' icon-fullscreen', u'Лаборатория'),
        ('lab:journal',' icon-book', u'Журнал'),
        ('lab:stats',' icon-signal', u'Характеристики'),
    ),
    make = (
        ('make:index', 'icon-tasks', u'Производство'),
        ('make:warren', 'icon-resize-full', u'Садка за день'),
        )
)
menu = dict(
    energy=(
        ('energy:Energy-add', 'icon-Energy', u'Энергоресурсы'),
        ('energy:Teplo-add', 'icon-Teplo', u'Тепло'),
        ),
    it=(
        ('it:Device-add', 'icon-inbox', 'Устройство или картридж'),
        ('it:Buy-add', 'icon-tint', 'Накладную'),
        ('it:Plug-add', 'icon-adjust', 'Замену'),
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
        ('make:Forming-add','',u'Формовка'),
        ('make:Warren-add','',u'Садка'),
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
