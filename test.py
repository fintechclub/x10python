import json
import pprint
import time
import operator

a = {}


a['1'] = (2, 1)

a['2'] = (5, 5)

a['1'] = tuple(map(lambda q, a: q + a, a['1'], (2, 1)))

print(  sum(x[1] for x in a.values()) )



