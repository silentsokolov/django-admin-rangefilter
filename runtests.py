#!/usr/bin/env python

from __future__ import unicode_literals

import django

from django.conf import settings
from django.core.management import call_command


settings.configure(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.sessions',
        'rangefilter',
    ),
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3'}
    },
    TEST_RUNNER='django.test.runner.DiscoverRunner',
    USE_TZ=True,
    TIME_ZONE='UTC',
)

django.setup()

if __name__ == '__main__':
    call_command('test', 'rangefilter')
