# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django
from django.template import Library

if django.VERSION[:2] >= (1, 10):
    from django.templatetags.static import static as _static  # pylint: disable-all
else:
    from django.contrib.admin.templatetags.admin_static import (
        static as _static,  # pylint: disable-all
    )

register = Library()


@register.simple_tag()
def static(path):
    return _static(path)
