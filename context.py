# -*- coding: utf-8 -*-
from whs.models import Brick

def bricks(request):
    if getattr(request,'namespace',None) == 'whs':
        Bricks = Brick.objects.all()
        return dict(Bricks=Bricks)
    return {}

nav = dict(
    main= (
        ('whs:Brick-list', 'icon-align-justify icon-white', u'Склад'),
        ('lab:index', 'icon-fullscreen icon-white', u'Лаборатория'),
        ('energy:index', 'icon-energy icon-white', u'Энергоресурсы'),
        ('it:index', 'icon-hdd icon-white', u'ИТ'),
        ('price', 'icon-shopping-cart icon-white', u'Прайс'),
    ),
    whs=(
        ('whs:Brick-list', 'icon-align-justify icon-white', u'Склад'),
        ('divider',),
        ('whs:Bill-list', 'icon-whs icon-white', u'Реализация'),
        ('whs:Add-list', 'icon-man icon-white', u'Производство'),
        ('divider',),
        ('whs:Agent-list', 'icon-Agent icon-white', u'Контрагенты'),
        ),
    it=(
        ('it:index', 'icon-hdd icon-white', u'ИТ'),
        ),
    energy=(
        ('energy:index', 'icon-energy icon-white', u'Энергоресурсы'),
        ('divider',),
        ('energy:Energy', 'icon-Energy icon-white', u'Энергия'),
        ('energy:Teplo', 'icon-Teplo icon-white', u'Тепло'),
        ),
    lab = (
        ('lab:index','icon-white icon-fullscreen', u'Лаборатория'),
    )
)
menu = dict(
    energy=(
        ('energy:Energy-add', 'icon-Energy', u'Энергоресурсы'),
        ('energy:Teplo-add', 'icon-Teplo', u'Тепло'),
        ),
    it=(
        ('it:Device-add', 'icon-inbox', 'Устройство или картридж'),
        ('it:Work-add', 'icon-headphones', 'Заявку'),
        ('it:Buy-add', 'icon-tint', 'Накладную'),
        ('it:Plug-add', 'icon-adjust', 'Замену'),
        ),
    whs=(
        ('whs:Bill-wizard', 'icon-Bill', u'Накладную'),
        ('whs:Add-add', 'icon-Man', u'Производство'),
        ('whs:Sorting-add', 'icon-Sorting', u'Сортировку'),
        ('whs:Inventory-add', 'icon-Inventory', u'Инвентаризацию'),
        ('divider',),
        ('whs:Brick-add', 'icon-Brick', u'Кирпич'),
        ('whs:Agent-add', 'icon-Agent', u'Контрагента'),
        ),
    lab = (
        ('lab:Clay-add','',u'Глина'),
        ('lab:StoredClay-add','',u'Глина по позициям'),
        ('lab:Sand-add','',u'Песок'),
        ('lab:Bar-add','',u'Брус'),
        ('lab:Raw-add','',u'Сырец'),
        ('lab:Batch-add','',u'Партия'),
        ('divider',),
        ('lab:WaterAbsorption-add','',u'Водопоглащение'),
        ('lab:Efflorescence-add','',u'Высолы'),
        ('lab:FrostResistance-add','',u'Морозостойкость'),
        ('lab:SEONR-add','',u'Уд.эф.акт.ест.рад.'),
        ('lab:HeatConduction-add','',u'Теплопроводность'),
        ('lab:Density-add','',u'Плотность'),
    ),
    cpu = (
        ('cpu:Device-add','',u'Устройство'),
        ('cpu:Position-add','',u'Канал')
    )
)
from django.core.urlresolvers import reverse
def namespace(request):
    namespace = getattr(request,'namespace',None) or 'main'
    return dict(nav=nav.get(namespace), menu=menu.get(namespace),current_app=namespace)
