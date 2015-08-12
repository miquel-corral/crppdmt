#annoyances/templatetags/data_verbose.py
from django import template

register = template.Library()

@register.simple_tag
def selected_option_text(bound_field, field_value):
    """
    Returns field's data or it's verbose version
    for a field with choices defined.

    Usage::

        {% load data_verbose %}
        {{form.some_field|data_verbose}}
    """

    field = bound_field.field

    #print dict(field.choices)
    #print("."+str(field_value)+".")
    #print(hasattr(field, 'choices'))
    #print(dict(field.choices).get(field_value, ''))

    # OBS: forced to int as key type to avoid random problems in getting option values
    return hasattr(field, 'choices') and dict(field.choices).get(int(field_value),'') or field_value
