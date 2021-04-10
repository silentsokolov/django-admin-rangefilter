# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings

warnings.warn(
    'Import from the `filter` module is deprecated. Use `filters` module.',
    DeprecationWarning
)

from .filters import DateRangeFilter, DateTimeRangeFilter
