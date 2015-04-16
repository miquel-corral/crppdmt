import datetime
from django import template

register = template.Library()

@register.assignment_tag(takes_context=True)
def set_context_var(context, name, value):
    """
    Set context variable
    :param name:
    :param value:
    :return:
    """
    context[name] = value
    return value

