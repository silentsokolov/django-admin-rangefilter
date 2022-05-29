# -*- coding: utf-8 -*-

from django.conf import settings

if not hasattr(settings, "ADMIN_RANGEFILTER_NONCE_ENABLED"):
    settings.ADMIN_RANGEFILTER_NONCE_ENABLED = True
