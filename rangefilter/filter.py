# -*- coding: utf-8 -*-

import warnings

warnings.warn(
    "Import from the `filter` module is deprecated. Use `filters` module.",
    DeprecationWarning,
    stacklevel=2,
)

from .filters import DateRangeFilter, DateTimeRangeFilter  # noqa # pylint: disable=unused-import
