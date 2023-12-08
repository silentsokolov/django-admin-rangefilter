# -*- coding: utf-8 -*-

from django.db import models


class RangeModelDT(models.Model):
    created_at = models.DateTimeField()

    class Meta:
        ordering = ("created_at",)


class RangeModelD(models.Model):
    created_at = models.DateField()

    class Meta:
        ordering = ("created_at",)


class RangeModelFloat(models.Model):
    float_value = models.FloatField()

    class Meta:
        ordering = ("float_value",)
