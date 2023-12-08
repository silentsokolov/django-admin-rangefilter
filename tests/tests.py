# -*- coding: utf-8 -*-

import datetime

try:
    import pytz
except ImportError:
    pytz = None

from unittest import skipIf

import django
from django.contrib.admin import ModelAdmin, site
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.utils import timezone
from django.utils.encoding import force_str

from rangefilter.filters import (
    DateRangeFilter,
    DateTimeRangeFilter,
    NumericRangeFilter,
    OnceCallMedia,
)
from rangefilter.templatetags.rangefilter_compat import static

from .models import RangeModelD, RangeModelDT, RangeModelFloat


class RangeModelDTAdmin(ModelAdmin):
    list_filter = (("created_at", DateRangeFilter),)
    ordering = ("-id",)


class RangeModelDAdmin(ModelAdmin):
    list_filter = (("created_at", DateRangeFilter),)
    ordering = ("-id",)


class RangeModelDTTimeAdmin(ModelAdmin):
    list_filter = (("created_at", DateTimeRangeFilter),)
    ordering = ("-id",)


class RangeModelDTimeAdmin(ModelAdmin):
    list_filter = (("created_at", DateTimeRangeFilter),)
    ordering = ("-id",)


class RangeModelFloatAdmin(ModelAdmin):
    list_filter = (("float_value", NumericRangeFilter),)
    ordering = ("-id",)


def select_by(dictlist):
    return list(dictlist)[0]


class DateFuncTestCase(TestCase):
    def test_make_dt_aware_without_pytz(self):
        with override_settings(USE_TZ=False):
            now = datetime.datetime.now()
            date = DateRangeFilter.make_dt_aware(now, pytz.utc)

            self.assertEqual(date.tzinfo, None)
            self.assertTrue(timezone.is_naive(date))

    @skipIf(pytz is None, "install pytz")
    @skipIf(django.VERSION >= (4, 0, 0), "pytz not django >= 4")
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

    @skipIf(django.VERSION < (4, 0, 0), "timezone django < 4")
    def test_make_dt_aware(self):
        local_tz = timezone.get_current_timezone()
        now = datetime.datetime.now()
        date = DateRangeFilter.make_dt_aware(now, local_tz)

        self.assertEqual(date.tzinfo, local_tz)
        self.assertTrue(timezone.is_aware(date))

        now = timezone.now()
        date = DateRangeFilter.make_dt_aware(now, local_tz)
        self.assertEqual(date.tzinfo, local_tz)
        self.assertTrue(timezone.is_aware(date))


class DateRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.django_book = RangeModelDT.objects.create(created_at=timezone.now())
        self.djangonaut_book = RangeModelDT.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7)
        )

        self.django_book_date = RangeModelD.objects.create(created_at=timezone.now())
        self.djangonaut_book_date = RangeModelD.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7)
        )

        self.username = "foo"
        self.email = "bar@foo.com"
        self.password = "top_secret"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, "get_changelist_instance", None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request,
            model,
            modeladmin.list_display,
            modeladmin.list_display_links,
            modeladmin.list_filter,
            modeladmin.date_hierarchy,
            modeladmin.search_fields,
            modeladmin.list_select_related,
            modeladmin.list_per_page,
            modeladmin.list_max_show_all,
            modeladmin.list_editable,
            modeladmin,
        )

    def test_datefilter(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTAdmin(RangeModelDT, site)

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

    def test_datefilter_filtered(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTAdmin(RangeModelDT, site)

        request = request_factory.get(
            "/",
            {
                "created_at__range__gte": self.today,
                "created_at__range__lte": self.tomorrow,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "created-at")

    def test_datefilter_with_default(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTAdmin(RangeModelDT, site)
        modeladmin.get_rangefilter_created_at_default = lambda func: [  # pylint: disable=W0201
            self.today,
            self.tomorrow,
        ]

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")
        self.assertEqual(filterspec.default_gte, self.today)
        self.assertEqual(filterspec.default_lte, self.tomorrow)

    def test_datefilter_filtered_with_one_params(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTAdmin(RangeModelDT, site)

        request = request_factory.get("/", {"created_at__range__gte": self.today})
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "created-at")

    def test_datefilter_filtered_datefield(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDAdmin(RangeModelD, site)

        request = request_factory.get(
            "/",
            {
                "created_at__range__gte": self.today,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelD, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book_date])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "created-at")


class NumericRangeFilterTestCase(TestCase):
    def setUp(self):
        self.django_book = RangeModelFloat.objects.create(float_value=1)
        self.djangonaut_book = RangeModelFloat.objects.create(float_value=10)

        self.username = "foo"
        self.email = "bar@foo.com"
        self.password = "top_secret"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, "get_changelist_instance", None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request,
            model,
            modeladmin.list_display,
            modeladmin.list_display_links,
            modeladmin.list_filter,
            modeladmin.date_hierarchy,
            modeladmin.search_fields,
            modeladmin.list_select_related,
            modeladmin.list_per_page,
            modeladmin.list_max_show_all,
            modeladmin.list_editable,
            modeladmin,
        )

    def test_numericfilter(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelFloatAdmin(RangeModelFloat, site)

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelFloat, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "float value")

    def test_numericfilter_filtered(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelFloatAdmin(RangeModelFloat, site)

        request = request_factory.get(
            "/",
            {
                "float_value__range__gte": 1,
                "float_value__range__lte": 5.5,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelFloat, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "float value")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "float-value")

    def test_numericfilter_with_default(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelFloatAdmin(RangeModelFloat, site)
        modeladmin.get_rangefilter_float_value_default = lambda r: [  # pylint: disable=W0201
            1,
            20,
        ]

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelFloat, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "float value")
        self.assertEqual(filterspec.default_gte, 1)
        self.assertEqual(filterspec.default_lte, 20)

    def test_numericfilter_filtered_with_one_params(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelFloatAdmin(RangeModelFloat, site)

        request = request_factory.get(
            "/",
            {
                "float_value__range__lte": 5,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelFloat, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "float value")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "float-value")

    def test_numericfilter_custom_title(self):
        request_factory = RequestFactory()
        custom_title = "foo bar"
        modeladmin = RangeModelFloatAdmin(RangeModelFloat, site)
        modeladmin.get_rangefilter_float_value_title = (  # pylint: disable=W0201
            lambda r, f: custom_title
        )

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelFloat, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), custom_title)


class DateTimeRangeFilterTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date.today()
        self.max_time = datetime.datetime.combine(timezone.now(), datetime.time.max).time()
        self.min_time = datetime.datetime.combine(timezone.now(), datetime.time.min).time()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.one_week_ago = self.today - datetime.timedelta(days=7)

        self.django_book = RangeModelDT.objects.create(created_at=timezone.now())
        self.djangonaut_book = RangeModelDT.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7)
        )

        self.django_book_date = RangeModelD.objects.create(created_at=timezone.now())
        self.djangonaut_book_date = RangeModelD.objects.create(
            created_at=timezone.now() - datetime.timedelta(days=7)
        )

        self.username = "foo"
        self.email = "bar@foo.com"
        self.password = "top_secret"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def get_changelist(self, request, model, modeladmin):
        if getattr(modeladmin, "get_changelist_instance", None):
            return modeladmin.get_changelist_instance(request)

        return ChangeList(
            request,
            model,
            modeladmin.list_display,
            modeladmin.list_display_links,
            modeladmin.list_filter,
            modeladmin.date_hierarchy,
            modeladmin.search_fields,
            modeladmin.list_select_related,
            modeladmin.list_per_page,
            modeladmin.list_max_show_all,
            modeladmin.list_editable,
            modeladmin,
        )

    def test_datetimefilter(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTTimeAdmin(RangeModelDT, site)

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

    def test_datetimefilter_filtered(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTTimeAdmin(RangeModelDT, site)

        request = request_factory.get(
            "/",
            {
                "created_at__range__gte_0": self.today,
                "created_at__range__gte_1": self.min_time,
                "created_at__range__lte_0": self.tomorrow,
                "created_at__range__lte_1": self.max_time,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "created-at")

    def test_datetimefilter_with_default(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTTimeAdmin(RangeModelDT, site)
        modeladmin.get_rangefilter_created_at_default = lambda r: [  # pylint: disable=W0201
            self.today,
            self.tomorrow,
        ]

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")
        self.assertEqual(filterspec.default_gte, self.today)
        self.assertEqual(filterspec.default_lte, self.tomorrow)

    def test_datetimefilter_filtered_with_one_params(self):
        request_factory = RequestFactory()
        modeladmin = RangeModelDTTimeAdmin(RangeModelDT, site)

        request = request_factory.get(
            "/",
            {
                "created_at__range__gte_0": self.today,
                "created_at__range__gte_1": self.min_time,
            },
        )
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), "created at")

        choice = select_by(filterspec.choices(changelist))
        self.assertEqual(choice["query_string"], "?")
        self.assertEqual(choice["system_name"], "created-at")

    def test_datetimefilter_custom_title(self):
        request_factory = RequestFactory()
        custom_title = "foo bar"
        modeladmin = RangeModelDTTimeAdmin(RangeModelDT, site)
        modeladmin.get_rangefilter_created_at_title = (  # pylint: disable=W0201
            lambda r, f: custom_title
        )

        request = request_factory.get("/")
        request.user = self.user

        changelist = self.get_changelist(request, RangeModelDT, modeladmin)

        queryset = changelist.get_queryset(request)

        self.assertEqual(list(queryset), [self.djangonaut_book, self.django_book])
        filterspec = changelist.get_filters(request)[0][0]
        self.assertEqual(force_str(filterspec.title), custom_title)


class TemplateTagsTestCase(TestCase):
    @override_settings(STATIC_URL="/test/")
    def test_returns_static_path_to_asset_when_staticfiles_app_is_not_installed(self):
        self.assertEqual(static("path"), "/test/path")

    def test_returns_static_path_to_asset_when_staticfiles_app_is_installed(self):
        with self.modify_settings(
            INSTALLED_APPS={
                "append": "django.contrib.staticfiles",
            }
        ):
            old_url = staticfiles_storage.base_url
            staticfiles_storage.base_url = "/test/"
            try:
                self.assertEqual(static("path"), "/test/path")
            finally:
                staticfiles_storage.base_url = old_url


class OnceCallMediaTestCase(TestCase):
    def setUp(self):
        self.media = OnceCallMedia()

    def test_str(self):
        self.assertEqual(
            str(self.media),
            "['/static/admin/js/calendar.js', '/static/admin/js/admin/DateTimeShortcuts.js']",
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.media),
            "OnceCallMedia(js=['/static/admin/js/calendar.js', '/static/admin/js/admin/DateTimeShortcuts.js'])",
        )

    def test_call(self):
        self.assertFalse(self.media._is_rendered)  # pylint: disable=protected-access
        self.assertNotEqual(self.media(), [])
        self.assertTrue(self.media._is_rendered)  # pylint: disable=protected-access
        self.assertEqual(self.media(), [])
