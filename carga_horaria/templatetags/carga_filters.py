from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def to_chrono(value):
    minutes = value * 45
    minutes_remaining = minutes % 60
    hours = (minutes - minutes_remaining) / 60
    return "%d:%02d" % (hours, minutes_remaining)

@register.filter
def hhmm(value):
    hours = value
    minutes = 60 * (hours % 1)
    return "%d:%02d" % (hours, minutes)

@register.filter
def decimal_maybe(value):
    if value % 1 == 0:
        return int(value)
    else:
        return "{:.1f}".format(value).replace('.', ',')
