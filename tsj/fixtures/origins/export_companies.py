#!/usr/bin/python
from json import dumps as jdumps
from sys import stdin, argv
from itertools import count
from pprint import PrettyPrinter
from collections import OrderedDict

def order_dict(keys, d):
    return OrderedDict([(k, d[k]) for k in keys])

ENTITY_ORDER = ("model", "pk", "fields")
USER_ORDER = (
    "username",
    "first_name",
    "last_name",
    "is_active",
    "is_superuser",
    "is_staff",
    "last_login",
    "groups",
    "user_permissions",
    "password",
    "email",
    "date_joined")

COMPANY_ORDER = (
    "name",
    "full_name",
    "workgraph",
    "company_type",
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
    "proof",
    "user",
    "orgn",
    "orgn_emitter",
    "email",
    "bill_numb")

j = []
lines = stdin.readlines()
for s, i in zip(lines, count(1)):
    vals = s.strip()[1:-1].split('","')
    user = order_dict(ENTITY_ORDER, {
        "model": "auth.user",
        "pk": i,
        "fields": order_dict(USER_ORDER, {
            "username": "testcom"+str(i),
            "first_name": "",
            "last_name": "",
            "is_active": True,
            "is_superuser": True,
            "is_staff": True,
            "last_login": "2014-10-17T19:40:23.371Z",
            "groups": [],
            "user_permissions": [],
            "password": "pbkdf2_sha256$12000$vxQhU3S5NDLt$SxI8swzmISd0c2lN2wyDrE4pt72s8ZB1NqHwQOf7uNU=",
            "email": "testcom@test.test",
            "date_joined": "2014-10-17T19:40:08.944Z"
        })
    })

    entity = order_dict(ENTITY_ORDER, {
        "model": "tsj.company",
        "pk": i,
        "fields": {
            "kpp": "12345654321",
            "bank_name": "12343543",
            "kor_schet": "2342342343",
            "orgn_date": "2014-10-10",
            "bik": "3424234324",
            "boss_fio": "\u0419\u0446\u0443\u043a \u0415\u043d\u0433 \u0418\u0447\u0435\u0448\u0443\u0442\u0441\u044f",
            "phone": "777771",
            "inn": "123123213123213",
            "proof": "scans/\u043f\u0430\u0441\u043f\u043e\u0440\u0442_HZzLWaq.png",
            "user": i,
            "orgn": "123213213213123",
            "orgn_emitter": "\u0439\u0446\u0443\u043a\u0435\u043d\u043a\u0443\u0446\u0439",
            "email": "takie@dela.test",
            "bill_numb": "1123213123"
        }
    })

    entity['fields'] = order_dict(COMPANY_ORDER, dict({
        'name': vals[0],
        'full_name': vals[0],
        'workgraph': vals[1],
        'company_type': 0 if int(vals[2]) <800 else 1,
        'post_address': vals[3],
        'legal_address': vals[3]
    }, **entity['fields']))
    j += [user, entity]

pp = PrettyPrinter(indent=4)
print('s = ')
pp.pprint(j)

if(len(argv) > 1):
    jf = open(argv[1], 'w')
    jf.writelines(jdumps(j, indent=4))
    jf.close()