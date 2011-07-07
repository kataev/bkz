#-*- coding: utf-8 -*-
#from django.http import HttpResponse
#from django.template.loader import render_to_string
#from cjson import encode as json
#import datetime
#import csv
#from django.db.models import Count

#from whs.bricks.models import *

#def show_tree(request):
#    store = MPTreeStore()
#    return HttpResponse(store.to_json(), mimetype='application/json')
#
#def show_brick(request):
#    store = BrickStore()
#    return HttpResponse(store.to_json(), mimetype='application/json')
#
#
#
#def fill_tree(request):
#    get = lambda node_id: Category.objects.get(pk=node_id)
#    root = Category.add_root(name=bricks._meta.verbose_name,count=0)
#    a = True
#    for cl in bricks.objects.values('brick_class').annotate(count=Count('brick_class')).order_by():
#        if a:
#            b = get(root.id).add_child(name=cl['brick_class'],count=int(cl['count']))
#            a=False
#        else:
#            cl_node = get(b.id).add_sibling(name=cl['brick_class'],count=int(cl['count']))
#
##        for w in bricks.objects.values('weight').annotate(count=Count('weight')).order_by():
##            w_node = get(cl_node.id).add_child(name=w['weight'],count=int(w['count']))
##
##            for v in bricks.objects.values('view').annotate(count=Count('view')).order_by():
##                v_node = get(w_node.id).add_child(name=v['view'],count=int(v['count']))
##
###                for m in bricks.objects.values('mark').annotate(count=Count('mark')).order_by():
###                    m_node = get(v_node.id).add_child(name=m['mark'],count=int(m['count']))
#
#    store = MPTreeStore(is_nested=True)
#    return HttpResponse(store.to_json(), mimetype='application/json')