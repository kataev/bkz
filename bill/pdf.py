# -*- coding: utf-8 -*-
import re

from django.http import QueryDict,HttpResponse
from django.template import loader, Context

import trml2pdf


# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' +\
                 u'|' +\
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' %\
                 (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                  unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                  unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))

def pdf_render_to_response(template, context, filename=None, prompt=False):
    response = HttpResponse(mimetype='application/pdf')
    if not filename:
        filename = template+'.pdf'
    cd = []
    if prompt:
        cd.append('attachment')
    cd.append('filename=%s' % filename)
    response['Content-Disposition'] = '; '.join(cd)
    tpl = loader.get_template(template)
    tc = {'filename': filename}
    tc.update(context)
    ctx = Context(tc)

    x = tpl.render(ctx)
    x = re.sub(RE_XML_ILLEGAL, "?", x)

    pdf = trml2pdf.parseString(x.encode("utf-8"))
    response.write(pdf)
    return response