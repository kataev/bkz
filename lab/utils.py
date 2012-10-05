import re

tto_regexp = re.compile(r'(?:(\d+)-?(\d*))+')

def convert_tto(tto):
    """ Split '12-25,11' to array """
    return sum([range(int(b), int(e or b) + 1) for b,e in tto_regexp.findall(tto)],[])


def get_min_avg_max(tests):
    tests = [t.value for t in tests]
    if tests:
        return min(tests),sum(tests)/len(tests),max(tests)
    else:
        return 0,0,0