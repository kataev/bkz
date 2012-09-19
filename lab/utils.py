import re

tto_regexp = re.compile(r'(?:(\d+)-?(\d*))+')

def _get_tto(t):
    b,e = t
    if e: return range(int(b),int(e)) + [int(e),]
    else: return [int(b),]

get_tto = lambda tto: sorted(sum(map(_get_tto,tto_regexp.findall(tto)),[]))
