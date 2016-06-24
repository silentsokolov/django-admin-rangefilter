.. image:: https://travis-ci.org/silentsokolov/django-admin-rangefilter.png?branch=master
   :target: https://travis-ci.org/silentsokolov/django-admin-rangefilter


django-admin-rangefilter
========================

django-admin-rangefilter app, add the filter by a custom date range on the admin UI.

.. image:: https://raw.githubusercontent.com/silentsokolov/django-admin-rangefilter/master/docs/images/screenshot.png


Requirements
------------

* Python 2.7+ or Python 3.2+
* Django 1.7+


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
    from rangefilter.filtres import DateRangeFilter

    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_filter = (
            ('created_at', DateRangeFilter), ('updated_at', DateRangeFilter),
        )
