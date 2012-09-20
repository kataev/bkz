import re

tto_regexp = re.compile(r'(?:(\d+)-?(\d*))+')

def get_tto(tto):
    """ Split '12-25,11' to array """
    return sum([range(int(b), int(e or b) + 1) for b,e in tto_regexp.findall(tto)],[])
