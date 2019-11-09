# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

try:
    import pytz
except ImportError:
    pytz = None

from unittest import skipIf

from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.db import models
from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.contrib.staticfiles.storage import staticfiles_storage

from .filter import DateRangeFilter, DateTimeRangeFilter
from .templatetags.rangefilter_compat import static


class MyModel(models.Model):
    created_at = models.DateTimeField()

    class Meta:
        ordering = ('created_at',)


class MyModelDate(models.Model):
    created_at = models.DateField()

    class Meta:
        ordering = ('created_at',)


class MyModelAdmin(ModelAdmin):
    list_filter = (('created_at', DateRangeFilter),)
    ordering = ('-id',)


class MyModelDateAdmin(ModelAdmin):
    list_filter = (('created_at', DateRangeFilter),)
    ordering = ('-id',)


class MyModelTimeAdmin(ModelAdmin):
    list_filter = (('created_at', DateTimeRangeFilter),)
    ordering = ('-id',)


class MyModelDateTimeAdmin(ModelAdmin):
    list_filter = (('created_at', DateTimeRangeFilter),)
    ordering = ('-id',)


def select_by(dictlist):
    return [x for x in dictlist][0]


class DateFuncTestCase(TestCase):
    def test_make_dt_aware_without_pytz(self):
        with override_settings(USE_TZ=False):
            now = datetime.datetime.now()
            date = DateRangeFilter.make_dt_aware(now, None)

            self.assertEqual(date.tzinfo, None)
            self.assertTrue(timezone.is_naive(date))

    @skipIf(pytz is None, 'install pytz')
    def test_make_dt_aware_with_pytz(self):
        local_tz = timezone.get_current_timezone()
        now = datetime.datetime.now()
        date = DateRangeFilter.make_dt_aware(now, local_tz)

        self.assertEqual(date.tzinfo.zone, local_tz.zone)
        self.assertTrue(timezone.is_aware(date))

        now = timezone.now()
        date = DateRangeFilter.make_dt_aware(now, local_tz)
        self.assertEqual(date.tzinfo.zone, local_tz.zone)
        self.assertTrue(timezone.is_aware(date))


class DateRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.django_book = MyModel.objects.create(created_at=timezone.now())
        self.djangonaut_book = MyModel.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7))

        self.django_book_date = MyModelDate.objects.create(created_at=timezone.now())
        self.djangonaut_book_date = MyModelDate.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7))

        self.user = User.objects.create_user(username='test', password='top_secret')

    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, 'get_changelist_instance', None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
        )

    def test_datefilter(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

    def test_datefilter_filtered(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__range__gte': self.today,
                                                 'created_at__range__lte': self.tomorrow})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')

    def test_datefilter_filtered_with_one_params(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__range__gte': self.today})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')

    def test_datefilter_filtered_datefield(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelDateAdmin(MyModelDate, site)

        request = self.request_factory.get('/', {'created_at__range__gte': self.today,
                                                 'created_at__range__lte': self.tomorrow})
        request.user = self.user

        changelist = self.get_changelist(request, MyModelDate, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book_date])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')


class DateTimeRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.max_time = datetime.datetime.combine(timezone.now(), datetime.time.max).time()
        self.min_time = datetime.datetime.combine(timezone.now(), datetime.time.min).time()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.django_book = MyModel.objects.create(created_at=timezone.now())
        self.djangonaut_book = MyModel.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7))

        self.django_book_date = MyModelDate.objects.create(created_at=timezone.now())
        self.djangonaut_book_date = MyModelDate.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7))

        self.user = User.objects.create_user(username='test', password='top_secret')

    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, 'get_changelist_instance', None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request, model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable, modeladmin,
        )

    def test_datetimfilter(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelTimeAdmin(MyModel, site)

        request = self.request_factory.get('/')
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

    def test_datetimfilter_filtered(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelTimeAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__range__gte_0': self.today,
                                                 'created_at__range__gte_1': self.min_time,
                                                 'created_at__range__lte_0': self.tomorrow,
                                                 'created_at__range__lte_1': self.max_time})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')

    def test_datefilter_filtered_with_one_params(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelTimeAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__range__gte_0': self.today,
                                                 'created_at__range__gte_1': self.min_time})
        request.user = self.user

        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')


class TemplateTagsTestCase(TestCase):
    @override_settings(STATIC_URL='/test/')
    def test_returns_static_path_to_asset_when_staticfiles_app_is_not_installed(self):
        self.assertEqual(static('path'), '/test/path')

    def test_returns_static_path_to_asset_when_staticfiles_app_is_installed(self):
        with self.modify_settings(INSTALLED_APPS={
            'append': 'django.contrib.staticfiles',
        }):
            old_url = staticfiles_storage.base_url
            staticfiles_storage.base_url = '/test/'
            try:
                self.assertEqual(static('path'), '/test/path')
            finally:
                staticfiles_storage.base_url = old_url
