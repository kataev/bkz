# -*- coding: utf-8 -*-
from whs.brick.models import Brick
from django.core.urlresolvers import resolve, Resolver404

def bricks(request):
    Bricks = Brick.objects.all()
    return dict(Bricks=Bricks)



nav = dict(
    brick=(
        ('sale:main','icon-sale icon-white',u'Реализация'),
            ('divider-vertical',),
        ('man:main','icon-man icon-white',u'Производство'),
        ),
    sale=(
        ('brick:main','icon-align-justify icon-white',u'Склад'),
        ('sale:main','icon-sale icon-white',u'Накладные'),
        ('sale:agents','icon-Agent icon-white',u'Контрагенты'),
        ('sale:statistics','icon-signal icon-white',u'Статистика')
    ),
    man=(
        ('brick:main','icon-align-justify icon-white',u'Склад'),
        ('divider-vertical',),
        ('man:main','icon-jurnal icon-white',u'Журнал'),
    ),
    it=(
        ('it:main','icon-hdd icon-white',u'ИТ'),
    ),
    energy=(
        ('energy:main','icon-energy icon-white',u'Энергоресурсы'),
        ('divider-vertical',),
        ('energy:Energy','icon-Energy icon-white',u'Энергия'),
        ('energy:Teplo','icon-Teplo icon-white',u'Тепло'),
    )
)

menu = dict(
    energy=(
        ('energy:Energy','icon-Energy',u'Энергоресурсы'),
        ('energy:Teplo','icon-Teplo',u'Тепло'),
    ),
    it=(
        ('it:Device','icon-inbox','Устройство'),
        ('it:Work','icon-headphones','Заявку'),
        ('it:Buy','icon-tint','Расходник'),
        ('it:Plug','icon-adjust','Замену'),
    ),
    man=(
        ('sale:Bill','icon-Bill',u'Накладную'),
        ('man:Man','icon-Man',u'Производство'),
        ('man:Sort','icon-Sorting',u'Сортировку'),
        ('man:Inverntory','icon-Inventory',u'Инвентаризацию'),
        ('divider-vertical',),
        ('brick:Brick','icon-Brick',u'Кирпич'),
        ('sale:Agent','icon-Agent',u'Контрагента'),
    )

)
#    {% if namespace == 'energy' %}
#<li><a href="{% url 'energy:Energy' date %}"><i class='icon-Energy'></i> Энергоресурсы</a></li>
#<li><a href="{% url 'energy:Teplo' date %}"><i class='icon-Teplo'></i> Тепло</a></li>
#    {% elif namespace == 'it' %}
#<li><a href="{% url 'it:Device' id %}"><i class='icon-inbox'></i> Устройство</a></li>
#<li><a href="{% url 'it:Work' id %}"><i class='icon-headphones'></i> Заявку</a></li>
#<li><a href="{% url 'it:Buy' id %}"><i class='icon-tint'></i> Расходники</a></li>
#<li><a href="{% url 'it:Plug' id %}"><i class='icon-adjust'></i> Установку расходника</a></li>
#    {% else %}
#<li><a href="{% url 'sale:Bill' %}"><i class='icon-Bill'></i> Накладную</a></li>
#<li><a href="{% url 'man:Man' %}"><i class='icon-Man'></i> Производство</a></li>
#<li><a href="{% url 'man:Sort' %}"><i class='icon-Sorting'></i> Сортировку кирпича</a></li>
#<li><a href="{% url 'man:Inventory' %}"><i class='icon-Inventory'></i> Инвентаризацию</a></li>
#<li class="divider"></li>
#<li><a href="{% url 'brick:Brick' id %}"><i class='icon-Brick'></i> Кирпич</a></li>
#<li><a href="{% url 'sale:Agent' id %}"><i class='icon-Agent'></i> КонтрАгента</a></li>
#    {% endif %}
def namespace(request):
    try:
        url = resolve(request.path)
        return dict(nav=nav.get(url.namespace,[]),menu=menu.get(url.namespace,[]))
    except Resolver404:
        return dict()
