from django import template

register = template.Library()

@register.filter
def beauty_none(value):
    if value == None or value == '':
        return 'No especificado'
    else:
        return value
