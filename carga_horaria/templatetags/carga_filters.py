from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def hhmm(value):
    hours = value
    minutes = Decimal('60.00') * (hours % 1)
    return "%d:%02d" % (hours, minutes)


@register.filter
def decimal_maybe(value):
    if value % 1 == 0:
        return int(value)
    else:
        return "{:.1f}".format(value).replace('.', ',')
