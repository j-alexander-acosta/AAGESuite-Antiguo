from django import template

register = template.Library()

@register.filter
def hhmm(value):
    hours = value
    minutes = 60 * (hours % 1)
    return "%d:%02d" % (hours, minutes)
