# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def years_ru(value):
    try:
        v = int(value)
        if v % 10 == 0:
            return u'лет'
        elif 10 < v < 20:
            return u'лет'
        elif v % 10 == 1:
            return u'год'
        elif v % 10 in [2, 3, 4]:
            return u'года'
        else:
            return u'лет'

    except ValueError:
        return "ValueError"


register.filter('years_ru', years_ru)