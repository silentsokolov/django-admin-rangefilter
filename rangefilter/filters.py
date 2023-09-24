# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

import django

try:
    import pytz
except ImportError:
    pytz = None

try:
    import csp
except ImportError:
    csp = None

from collections import OrderedDict

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import AdminSplitDateTime as BaseAdminSplitDateTime
from django.template.defaultfilters import slugify
from django.templatetags.static import StaticNode
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.html import format_html

if django.VERSION >= (2, 0, 0):
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _  # pylint: disable=E0611


class OnceCallMedia(object):
    _is_rendered = False

    def __str__(self):
        return str([str(s) for s in self._js])

    def __repr__(self):
        return "OnceCallMedia(js=%r)" % ([str(s) for s in self._js])

    def __call__(self):
        if self._is_rendered:
            return []

        self._is_rendered = True
        return self._js

    def get_js(self):
        return [
            StaticNode.handle_simple("admin/js/calendar.js"),
            StaticNode.handle_simple("admin/js/admin/DateTimeShortcuts.js"),
        ]

    _js = property(get_js)


class AdminSplitDateTime(BaseAdminSplitDateTime):
    def format_output(self, rendered_widgets):
        return format_html(
            '<p class="datetime">{}</p><p class="datetime rangetime">{}</p>',
            rendered_widgets[0],
            rendered_widgets[1],
        )


class BaseRangeFilter(admin.filters.FieldListFilter):  # pylint: disable=abstract-method
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = "{0}__range__gte".format(field_path)
        self.lookup_kwarg_lte = "{0}__range__lte".format(field_path)

        super(BaseRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )

        self.default_gte, self.default_lte = self._get_default_values(
            request, model_admin, field_path
        )
        self.title = self._get_default_title(request, model_admin, field_path)

        self.request = request
        self.model_admin = model_admin
        self.form = self.get_form(request)

    def _get_default_title(self, request, model_admin, field_path):
        if hasattr(self, "__from_builder"):
            return self.default_title or self.title

        title_method_name = "get_rangefilter_{0}_title".format(field_path)
        title_method = getattr(model_admin, title_method_name, None)

        if not callable(title_method):
            return self.title

        return title_method(request, field_path)

    def _get_default_values(self, request, model_admin, field_path):
        if hasattr(self, "__from_builder"):
            return self.default_start, self.default_end

        default_method_name = "get_rangefilter_{0}_default".format(field_path)
        default_method = getattr(model_admin, default_method_name, None)

        if not callable(default_method):
            return None, None

        return default_method(request)


class DateRangeFilter(BaseRangeFilter):
    _request_key = "DJANGO_RANGEFILTER_ADMIN_JS_LIST"

    def get_timezone(self, _request):
        return timezone.get_default_timezone()

    @staticmethod
    def make_dt_aware(value, tzname):
        if settings.USE_TZ:
            if django.VERSION <= (4, 0, 0) and pytz is not None:
                default_tz = tzname
                if value.tzinfo is not None:
                    value = default_tz.normalize(value)
                else:
                    value = default_tz.localize(value)
            else:
                value = value.replace(tzinfo=tzname)
        return value

    def choices(self, changelist):
        yield {
            # slugify converts any non-unicode characters to empty characters
            # but system_name is required, if title converts to empty string use id
            # https://github.com/silentsokolov/django-admin-rangefilter/issues/18
            "system_name": force_str(
                slugify(self.title) if slugify(self.title) else id(self.title)
            ),
            "query_string": changelist.get_query_string({}, remove=self._get_expected_fields()),
        }

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def expected_parameters(self):
        return self._get_expected_fields()

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params["{0}__gte".format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_gte, datetime.time.min),
                self.get_timezone(request),
            )
        if date_value_lte:
            query_params["{0}__lte".format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_lte, datetime.time.max),
                self.get_timezone(request),
            )

        return query_params

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(**self._make_query_filter(request, validated_data))
        return queryset

    def get_template(self):
        if django.VERSION[:2] <= (1, 8):
            return "rangefilter/date_filter_1_8.html"

        if csp and getattr(settings, "ADMIN_RANGEFILTER_NONCE_ENABLED", True):
            return "rangefilter/date_filter_csp.html"

        return "rangefilter/date_filter.html"

    template = property(get_template)

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    forms.DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("From date")}),
                        localize=True,
                        required=False,
                        initial=self.default_gte,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    forms.DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("To date")}),
                        localize=True,
                        required=False,
                        initial=self.default_lte,
                    ),
                ),
            )
        )

    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type(str("DateRangeForm"), (forms.BaseForm,), {"base_fields": fields})

        # lines below ensure that the js static files are loaded just once
        # even if there is more than one DateRangeFilter in use
        js_list = getattr(self.request, self._request_key, None)
        if not js_list:
            js_list = OnceCallMedia()
            setattr(self.request, self._request_key, js_list)

        form_class.js = js_list

        return form_class

    def get_form(self, _request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters or None)


class DateTimeRangeFilter(DateRangeFilter):
    def _get_expected_fields(self):
        expected_fields = []
        for field in [self.lookup_kwarg_gte, self.lookup_kwarg_lte]:
            for i in range(2):
                expected_fields.append("{}_{}".format(field, i))

        return expected_fields

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    forms.SplitDateTimeField(
                        label="",
                        widget=AdminSplitDateTime(attrs={"placeholder": _("From date")}),
                        localize=True,
                        required=False,
                        initial=self.default_gte,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    forms.SplitDateTimeField(
                        label="",
                        widget=AdminSplitDateTime(attrs={"placeholder": _("To date")}),
                        localize=True,
                        required=False,
                        initial=self.default_lte,
                    ),
                ),
            )
        )

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params["{0}__gte".format(self.field_path)] = self.make_dt_aware(
                date_value_gte, self.get_timezone(request)
            )
        if date_value_lte:
            query_params["{0}__lte".format(self.field_path)] = self.make_dt_aware(
                date_value_lte, self.get_timezone(request)
            )

        return query_params


class NumericRangeFilter(BaseRangeFilter):
    def get_template(self):
        return "rangefilter/numeric_filter.html"

    template = property(get_template)

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def expected_parameters(self):
        return self._get_expected_fields()

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    forms.FloatField(
                        label="",
                        widget=forms.NumberInput(attrs={"placeholder": _("From")}),
                        required=False,
                        localize=True,
                        initial=self.default_lte,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    forms.FloatField(
                        label="",
                        widget=forms.NumberInput(attrs={"placeholder": _("To")}),
                        localize=True,
                        required=False,
                        initial=self.default_lte,
                    ),
                ),
            )
        )

    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type(str("NumericRangeFilter"), (forms.BaseForm,), {"base_fields": fields})

        return form_class

    def get_form(self, _request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters or None)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(**self._make_query_filter(request, validated_data))
        return queryset

    def _make_query_filter(self, _request, validated_data):
        query_params = {}
        value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if value_gte is not None:
            query_params["{0}__gte".format(self.field_path)] = value_gte
        if value_lte is not None:
            query_params["{0}__lte".format(self.field_path)] = value_lte

        return query_params

    def choices(self, changelist):
        yield {
            "system_name": force_str(
                slugify(self.title) if slugify(self.title) else id(self.title)
            ),
            "query_string": changelist.get_query_string({}, remove=self._get_expected_fields()),
        }


def DateRangeFilterBuilder(title=None, default_start=None, default_end=None):
    filter_cls = type(
        str("DateRangeFilter"),
        (DateRangeFilter,),
        {
            "__from_builder": True,
            "default_title": title,
            "default_start": default_start,
            "default_end": default_end,
        },
    )

    return filter_cls


def DateTimeRangeFilterBuilder(title=None, default_start=None, default_end=None):
    filter_cls = type(
        str("DateTimeRangeFilter"),
        (DateTimeRangeFilter,),
        {
            "__from_builder": True,
            "default_title": title,
            "default_start": default_start,
            "default_end": default_end,
        },
    )

    return filter_cls


def NumericRangeFilterBuilder(title=None, default_start=None, default_end=None):
    filter_cls = type(
        str("NumericRangeFilter"),
        (NumericRangeFilter,),
        {
            "__from_builder": True,
            "default_title": title,
            "default_start": default_start,
            "default_end": default_end,
        },
    )

    return filter_cls


class DateRangeQuickSelectListFilter(admin.DateFieldListFilter, DateRangeFilter):
    template = "rangefilter/date_range_quick_select_list_filter.html"

    def expected_parameters(self):
        params = [self.lookup_kwarg_gte, self.lookup_kwarg_lte]
        if self.field.null:
            params.append(self.lookup_kwarg_isnull)
        return params

    def _make_query_filter(self, request, validated_data):
        query_params = super()._make_query_filter(request, validated_data)
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)
        if self.field.null:
            date_value_isnull = validated_data.get(self.lookup_kwarg_isnull, None)

            if date_value_isnull is not None and not any([date_value_lte, date_value_gte]):
                query_params[self.lookup_kwarg_isnull] = date_value_isnull

        return query_params

    def _get_form_fields(self):
        fields = super()._get_form_fields()
        if self.field.null:
            fields.update(
                OrderedDict(
                    (
                        (
                            self.lookup_kwarg_isnull,
                            forms.BooleanField(
                                label="",
                                localize=True,
                                required=False,
                                widget=forms.HiddenInput,
                            ),
                        ),
                    )
                )
            )
        return fields


def DateRangeQuickSelectListFilterBuilder(title=None, default_start=None, default_end=None):
    filter_cls = type(
        str("DateRangeQuickSelectListFilter"),
        (DateRangeQuickSelectListFilter,),
        {
            "__from_builder": True,
            "default_title": title,
            "default_start": default_start,
            "default_end": default_end,
        },
    )

    return filter_cls
