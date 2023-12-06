.. image:: https://github.com/EricOuma/django-jazzmin-admin-rangefilter/workflows/build/badge.svg?branch=master
   :target: https://github.com/EricOuma/django-jazzmin-admin-rangefilter/actions?query=workflow%3Abuild

.. image:: https://codecov.io/gh/EricOuma/django-jazzmin-admin-rangefilter/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/EricOuma/django-jazzmin-admin-rangefilter

django-jazzmin-admin-rangefilter
================================

A Django app that adds a filter by date range and numeric range to the Django Jazzmin admin UI.

.. image:: https://raw.githubusercontent.com/EricOuma/django-jazzmin-admin-rangefilter/master/docs/images/screenshot.png


Requirements
------------

* Python 2.7+ or Python 3.6+
* Django 1.8+


Installation
------------

Use your favorite Python package manager to install the app from PyPI, e.g.

Example:

``pip install django-jazzmin-admin-rangefilter``


Add ``rangefilter`` to ``INSTALLED_APPS``:

Example:

.. code:: python

    INSTALLED_APPS = (
        ...
        'rangefilter',
        ...
    )


Example usage
-------------

In admin
~~~~~~~~

.. code:: python

    from datetime import datetime

    from django.contrib import admin
    from rangefilter.filters import (
        DateRangeFilterBuilder,
        DateTimeRangeFilterBuilder,
        NumericRangeFilterBuilder,
        DateRangeQuickSelectListFilterBuilder,
    )

    from .models import Post


    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_filter = (
            ("created_at", DateRangeFilterBuilder()),
            (
                "updated_at",
                DateTimeRangeFilterBuilder(
                    title="Custom title",
                    default_start=datetime(2020, 1, 1),
                    default_end=datetime(2030, 1, 1),
                ),
            ),
            ("num_value", NumericRangeFilterBuilder()),
            ("created_at", DateRangeQuickSelectListFilterBuilder()),  # Range + QuickSelect Filter
        )


Support Content-Security-Policy
-------------------------------

For Django 1.8+, if `django-csp <https://github.com/mozilla/django-csp>`_ is installed, nonces will be added to style and script tags.
The setting `ADMIN_RANGEFILTER_NONCE_ENABLED` controls this behavior.

.. code:: python

    INSTALLED_APPS = (
        ...
        'rangefilter',
        'csp',
        ...
    )
