# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

__author__ = 'Dmitriy Sokolov'
__version__ = '0.8.4'

if django.VERSION >= (3, 2):
    # The declaration is only needed for older Django versions
    pass
else:
    default_app_config = 'rangefilter.apps.RangeFilterConfig'


VERSION = __version__
