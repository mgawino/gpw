# -*- coding: utf-8 -*-
from datetime import datetime

from gpw.models import Company, Statistics


class CompanyPipeline:

    @staticmethod
    def _replace_blank_chars(value):
        if value is None:
            return None
        for blank in ('\n', '\t', ' ', '\xa0'):
            value = value.replace(blank, '')
        return value

    def process_item(self, item, spider):
        for attr_name in item:
            item[attr_name] = self._replace_blank_chars(item[attr_name])
        item['debut_date'] = datetime.strptime(item['debut_date'], '%m.%Y').date()
        item['total_actions'] = int(item['total_actions'])
        item['value'] = float(item['value'].replace(',', '.'))
        company = Company(**item)
        company.save()
        return item


class StatisticsPipeline:
    _CACHE_MAX_SIZE = 1000

    def __init__(self):
        self._stats_cache = []

    def _bulk_insert(self):
        Statistics.objects.bulk_create(self._stats_cache)
        self._stats_cache = []

    def process_item(self, item, spider):
        assert 'PLN' == item.pop('currency')
        item.pop('name')  # remove company name
        self._stats_cache.append(Statistics(**item))
        if len(self._stats_cache) >= self._CACHE_MAX_SIZE:
            self._bulk_insert()

    def close_spider(self, spider):
        if len(self._stats_cache) > 0:
            self._bulk_insert()
