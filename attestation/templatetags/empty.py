# -*- coding: utf-8 -*-
from django import template

register = template.Library()

def not_empty(value, arg):
    if value is not None:
        return "%s %s" % (arg, value)
    else:
        return ""


register.filter('not_empty', not_empty)