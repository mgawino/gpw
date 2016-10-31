# -*- coding: utf-8 -*-
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=10, unique=True)
    currency = models.CharField(max_length=3)


class Statistics(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='statistics',
        unique_for_date='date',
    )
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    max_price = models.FloatField()
    min_price = models.FloatField()
    nominal_price = models.FloatField()
    market_money = models.FloatField()
    volume = models.FloatField()
    open_positions = models.IntegerField()
    open_positions_value = models.FloatField()
    changes = models.FloatField()
    transactions_num = models.IntegerField()
