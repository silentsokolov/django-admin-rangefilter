# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.db import models
from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.views.main import ChangeList
from django.utils.encoding import force_text

from .filter import make_dt_aware, DateRangeFilter


class MyModel(models.Model):
    created_at = models.DateTimeField()

    class Meta:
        ordering = ('created_at',)


class MyModelAdmin(ModelAdmin):
    list_filter = (('created_at', DateRangeFilter),)
    ordering = ('-id',)


def select_by(dictlist):
    return [x for x in dictlist][0]


class DateFuncTestCase(TestCase):
    def test_make_dt_aware_without_pytz(self):
        with override_settings(USE_TZ=False):
            now = datetime.datetime.now()
            date = make_dt_aware(now)

            self.assertEqual(date.tzinfo, None)
            self.assertTrue(timezone.is_naive(date))

    def test_make_dt_aware_with_pytz(self):
        local_tz = timezone.get_current_timezone()
        now = datetime.datetime.now()
        date = make_dt_aware(now)

        self.assertEqual(date.tzinfo.zone, local_tz.zone)
        self.assertTrue(timezone.is_aware(date))

        now = timezone.now()
        date = make_dt_aware(now)

        self.assertEqual(date.tzinfo.zone, local_tz.zone)
        self.assertTrue(timezone.is_aware(date))


class DateRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.django_book = MyModel.objects.create(created_at=self.today)
        self.djangonaut_book = MyModel.objects.create(created_at=self.one_week_ago)

    def get_changelist(self, request, model, modeladmin):
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
        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

    def test_datefilter_filtered(self):
        self.request_factory = RequestFactory()
        modeladmin = MyModelAdmin(MyModel, site)

        request = self.request_factory.get('/', {'created_at__gte': self.today,
                                                 'created_at__lte': self.tomorrow})
        changelist = self.get_changelist(request, MyModel, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_text(filterspec.title), 'created at')

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice['query_string'], '?')
        self.assertEqual(choice['system_name'], 'created-at')
