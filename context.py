# -*- coding: utf-8 -*-
from whs.models import Brick

def bricks(request):
    if getattr(request,'namespace',None) == 'whs':
        Bricks = Brick.objects.all()
        return dict(Bricks=Bricks)
    return {}

nav = dict(
    main= (
        ('whs:main', 'icon-align-justify icon-white', u'Склад'),
        ('lab:main', 'icon-fullscreen icon-white', u'Лаборатория'),
        ('energy:main', 'icon-energy icon-white', u'Энергоресурсы'),
        ('it:main', 'icon-hdd icon-white', u'ИТ'),
    ),
    whs=(
        ('whs:main', 'icon-align-justify icon-white', u'Склад'),
        ('divider',),
        ('whs:sale', 'icon-whs icon-white', u'Реализация'),
        ('whs:man', 'icon-man icon-white', u'Производство'),
        ('divider',),
        ('whs:agents', 'icon-Agent icon-white', u'Контрагенты'),
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
    whs=(
        ('whs:Bill', 'icon-Bill', u'Накладную'),
        ('whs:Man', 'icon-Man', u'Производство'),
        ('whs:Sorting', 'icon-Sorting', u'Сортировку'),
        ('whs:Inventory', 'icon-Inventory', u'Инвентаризацию'),
        ('divider',),
        ('whs:Brick', 'icon-Brick', u'Кирпич'),
        ('whs:Agent', 'icon-Agent', u'Контрагента'),
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
        ('lab:SEONR','',u'Уд.эф.акт.ест.рад.'),
        ('lab:HeatConduction','',u'Теплопроводность'),
        ('lab:Density','',u'Плотность'),
        ('lab:Batch','',u'Партия'),
    ),
    cpu = (
        ('cpu:Device','',u'Устройство'),
        ('cpu:Position','',u'Канал')
    )
)

def namespace(request):
    namespace = getattr(request,'namespace',None) or 'main'
    return dict(nav=nav.get(namespace), menu=menu.get(namespace))
