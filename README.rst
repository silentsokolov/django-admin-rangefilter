.. image:: https://travis-ci.org/silentsokolov/django-admin-rangefilter.svg?branch=master
   :target: https://travis-ci.org/silentsokolov/django-admin-rangefilter

.. image:: https://codecov.io/gh/silentsokolov/django-admin-rangefilter/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/silentsokolov/django-admin-rangefilter

django-admin-rangefilter
========================

django-admin-rangefilter app, add the filter by a custom date / datetime range on the admin UI.

.. image:: https://raw.githubusercontent.com/silentsokolov/django-admin-rangefilter/master/docs/images/screenshot.png


Requirements
------------

* Python 2.7+ or Python 3.4+
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
    from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

    from .models import Post


    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_filter = (
            ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
        )


Support Content-Security-Policy
-------------------------------

For Django 1.8+, if `django-csp <https://github.com/mozilla/django-csp>`_ is installed, nonces will be added to style and script tags.

.. code:: python

    INSTALLED_APPS = (
        ...
        'rangefilter',
        'csp',
        ...
    )
