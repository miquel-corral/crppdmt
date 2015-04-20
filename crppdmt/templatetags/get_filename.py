from django.template import Library

register = Library()

# filter to use with FileField to get the filename in templates

@register.filter
def get_filename(arg):
    return str(arg)
