from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RangeFilterConfig(AppConfig):
    name = 'rangefilter'
    verbose_name = _('Range Filter')
