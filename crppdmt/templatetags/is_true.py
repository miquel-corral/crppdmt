from django.template import Library

register = Library()

@register.filter
def is_true(arg):
    return arg is True
