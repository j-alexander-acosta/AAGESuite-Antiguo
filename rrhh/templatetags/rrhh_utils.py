from django import template

register = template.Library()


@register.filter
def beauty_none(value):
    if value is None or value == '':
        return 'No especificado'
    else:
        return value


@register.filter
def start_with(value, arg):
    return value.startswith(arg)


@register.filter
def get_word(value, arg):
    return value.split(' ')[int(arg) - 1]