# -*- coding: utf-8 -*-
from bkz.brick.models import Brick

def bricks(request):
    Bricks = Brick.objects.all()
    return dict(Bricks=Bricks)

nav = dict(
    brick=(
        ('sale:main', 'icon-sale icon-white', u'Реализация'),
        ('divider',),
        ('man:main', 'icon-man icon-white', u'Производство'),
        ),
    sale=(
        ('brick:main', 'icon-align-justify icon-white', u'Склад'),
        ('sale:main', 'icon-sale icon-white', u'Накладные'),
        ('sale:agents', 'icon-Agent icon-white', u'Контрагенты'),
        ('sale:statistics', 'icon-signal icon-white', u'Статистика')
        ),
    man=(
        ('brick:main', 'icon-align-justify icon-white', u'Склад'),
        ('divider',),
        ('man:main', 'icon-jurnal icon-white', u'Журнал'),
        ),
    it=(
        ('it:main', 'icon-hdd icon-white', u'ИТ'),
        ),
    energy=(
        ('energy:main', 'icon-energy icon-white', u'Энергоресурсы'),
        ('divider',),
        ('energy:Energy', 'icon-Energy icon-white', u'Энергия'),
        ('energy:Teplo', 'icon-Teplo icon-white', u'Тепло'),
        )
)
menu = dict(
    energy=(
        ('energy:Energy', 'icon-Energy', u'Энергоресурсы'),
        ('energy:Teplo', 'icon-Teplo', u'Тепло'),
        ),
    it=(
        ('it:Device', 'icon-inbox', 'Устройство'),
        ('it:Work', 'icon-headphones', 'Заявку'),
        ('it:Buy', 'icon-tint', 'Расходник'),
        ('it:Plug', 'icon-adjust', 'Замену'),
        ),
    brick=(
        ('sale:Bill', 'icon-Bill', u'Накладную'),
        ('man:Man', 'icon-Man', u'Производство'),
        ('man:Sort', 'icon-Sorting', u'Сортировку'),
        ('man:Inventory', 'icon-Inventory', u'Инвентаризацию'),
        ('divider',),
        ('brick:Brick', 'icon-Brick', u'Кирпич'),
        ('sale:Agent', 'icon-Agent', u'Контрагента'),
        ),
    lab = (
        ('lab:Clay','',u'Глина'),
        ('lab:StoredClay','',u'Глина по позициям'),
        ('lab:Sand','',u'Песок'),
        ('lab:Bar','',u'Брус'),
        ('lab:Raw','',u'Сырец'),
        ('lab:WaterAbsorption','',u'Водопоглащение'),
        ('lab:Efflorescence','',u'Высолы'),
        ('lab:FrostResistance','',u'Морозостойкость'),
        ('lab:Density','',u'Плотность'),
        ('lab:Batch','',u'Партия'),
    ),
    cpu = (
        ('cpu:Device','',u'Устройство'),
        ('cpu:Position','',u'Канал')
    )
)

def namespace(request):
    namespace = getattr(request,'namespace','')
    if namespace in 'sale man':
        namespace = 'brick'
    return dict(nav=nav.get(namespace, []), menu=menu.get(namespace, []))
