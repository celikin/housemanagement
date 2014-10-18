#!/usr/bin/python3
from itertools import chain, repeat
from json import dumps as jdumps
from sys import stdin, argv
from itertools import count
from pprint import PrettyPrinter
from collections import OrderedDict

def order_dict(keys, d):
    print(d)
    return OrderedDict([(k, d[k]) for k in keys])

def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip(*[chain(iterable, repeat(padvalue, n-1))]*n)

ENTITY_ORDER = ("model", "pk", "fields")

SERV_ORDER = (
    "name",
    "full_name",
    "workgraph",
    "post_address",
    "legal_address",
    "kpp",
    "bank_name",
    "kor_schet",
    "orgn_date",
    "bik",
    "boss_fio",
    "phone",
    "inn",
    "orgn",
    "orgn_emitter",
    "email",
    "bill_numb")

j = []
lines = grouper(4, stdin.readlines())
for s, i in zip(lines, count(1)):
    s = [i.strip() for i in s]
    entity = order_dict(ENTITY_ORDER, {
        "model": "tsj.servicecompany",
        "pk": i,
        "fields": {
            "workgraph": "Ежедневно 10:00-24:00",
            "kpp": "12345654321",
            "bank_name": "12343543",
            "kor_schet": "2342342343",
            "orgn_date": "2014-10-10",
            "bik": "3424234324",
            "boss_fio": "\u0419\u0446\u0443\u043a \u0415\u043d\u0433 \u0418\u0447\u0435\u0448\u0443\u0442\u0441\u044f",
            "phone": "777771",
            "inn": "123123213123213",
            "orgn": "123213213213123",
            "orgn_emitter": "\u0439\u0446\u0443\u043a\u0435\u043d\u043a\u0443\u0446\u0439",
            "email": "takie@dela.test",
            "bill_numb": "1123213123"
        }
    })

    entity['fields'] = order_dict(SERV_ORDER, dict({
        'name': s[0],
        'full_name': s[2],
        'post_address': s[3],
        'legal_address': s[3]
    }, **entity['fields']))
    j += [entity]

pp = PrettyPrinter(indent=4)
print('s = ')
pp.pprint(j)

if(len(argv) > 1):
    jf = open(argv[1], 'w')
    jf.writelines(jdumps(j, indent=4))
    jf.close()