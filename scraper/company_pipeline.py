# -*- coding: utf-8 -*-
from datetime import datetime

from gpw.models import Company


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