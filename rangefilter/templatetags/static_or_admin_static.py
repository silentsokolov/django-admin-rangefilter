import django
from django.template import Library

register = Library()


@register.simple_tag()
def static(path):
    if django.VERSION[:2] >= (1, 10):
        from django.templatetags.static import static as _static
    else:
        from django.contrib.admin.templatetags.admin_static import static as _static

    return _static(path)
