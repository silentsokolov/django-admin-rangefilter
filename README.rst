.. image:: https://github.com/silentsokolov/django-admin-rangefilter/workflows/build/badge.svg?branch=master
   :target: https://github.com/silentsokolov/django-admin-rangefilter/actions?query=workflow%3Abuild

.. image:: https://codecov.io/gh/silentsokolov/django-admin-rangefilter/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/silentsokolov/django-admin-rangefilter

django-admin-rangefilter
========================

A Django app that adds a filter by date range and numeric range to the admin UI.

.. image:: https://raw.githubusercontent.com/silentsokolov/django-admin-rangefilter/master/docs/images/screenshot.png


Requirements
------------

* Python 2.7+ or Python 3.6+
* Django 1.8+


Installation
------------

Use your favorite Python package manager to install the app from PyPI, e.g.

Example:

``pip install django-admin-rangefilter``


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

    from django.contrib import admin
    from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter

    from .models import Post


    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_filter = (
            ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
            ('num_value', NumericRangeFilter),
        )
        
        # If you would like to add a default range filter
        # method pattern "get_rangefilter_{field_name}_default"
        def get_rangefilter_created_at_default(self, request):
            return (datetime.date.today, datetime.date.today)

        # If you would like to change a title range filter
        # method pattern "get_rangefilter_{field_name}_title"
        def get_rangefilter_created_at_title(self, request, field_path):
            return 'custom title'


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
