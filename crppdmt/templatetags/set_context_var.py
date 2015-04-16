import datetime
from django import template

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_context_var(context, name):
    """
    Set context variable
    :param name:
    :return:
    """
    return context[name]

