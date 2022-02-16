# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django

from rangefilter import settings

__author__ = 'Dmitriy Sokolov'
__version__ = '0.8.3'

if django.VERSION < (3, 2):
    default_app_config = 'rangefilter.apps.RangeFilterConfig'


VERSION = __version__
