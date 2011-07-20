from django import template
#from templatetag_sugar.register import tag
#from templatetag_sugar.parser import Name, Variable, Constant, Optional, Model

register = template.Library()
def hash(h,key):
    if key in h:
#        print h[key]
        return h[key]
    else:
        return None

register.filter(hash)