import re

def stripped_lines(s):
    return tuple(l.strip() for l in s.split('\n'))
