# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

import requests
import xlrd
from django.core.management import BaseCommand
from gpw.models import Company, Statistics


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self._company_cache = {}

    def _get_company(self, **company_attrs):
        company_name = company_attrs['name']
        company = self._company_cache.get(company_name)
        if company is None:
            company, created = Company.objects.get_or_create(**company_attrs)
            self._company_cache[company_name] = company
        return company

    @staticmethod
    def _pop_company_attrs(statistics):
        statistics.pop('isin_code')  # not used
        return {
            'name': statistics.pop('name'),
            'currency': statistics.pop('currency'),
        }

    def handle(self, *args, **options):
        start_date = datetime(year=2014, month=1, day=1).date()
        end_date = datetime.today().date()
        downloader = GPWDataDownloader(start_date=start_date, end_date=end_date)
        all_stats = []
        for stats in downloader.iter_statistics():
            company_attrs = self._pop_company_attrs(stats)
            company = self._get_company(**company_attrs)
            statistics = Statistics(company=company, **stats)
            all_stats.append(statistics)
        Statistics.objects.bulk_create(all_stats)


class GPWDataDownloader:

    _GPW_URL_TEMPLATE = 'https://www.gpw.pl/notowania_archiwalne?type=10&date={date}&fetch.x=28&fetch.y=23'
    _COLUMN_TRANSLATION = {
        'Data': 'date',
        'Nazwa': 'name',
        'ISIN': 'isin_code',
        'Kurs otwarcia': 'open_price',
        'Kurs zamknięcia': 'close_price',
        'Kurs max': 'max_price',
        'Kurs min': 'min_price',
        'Cena nominalna': 'nominal_price',
        'Obrót': 'market_money',
        'Wolumen': 'volume',
        'Liczba otwartych pozycji': 'open_positions',
        'Wartość otwartych pozycji': 'open_positions_value',
        'Zmiana': 'changes',
        'Waluta': 'currency',
        'Liczba Transakcji': 'transactions_num'
    }

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _fetch_data_from_day(self, date):
        date_str = date.strftime("%Y-%m-%d")
        print('Fetching data from day {}'.format(date_str))
        gpw_url = self._GPW_URL_TEMPLATE.format(date=date_str)
        response = requests.get(gpw_url)
        response.raise_for_status()
        workbook = xlrd.open_workbook(file_contents=response.content)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.get_rows()
        try:
            header = next(rows)
        except StopIteration:
            print('Empty data')
            return []
        header = [cell.value for cell in header]
        # print(set(header) - set(self._COLUMN_TRANSLATION))
        assert set(header) == set(self._COLUMN_TRANSLATION)
        result = []
        for row in rows:
            row_values = [cell.value for cell in row]
            assert len(row_values) == len(header)
            row_dict = dict(zip(header, row_values))
            result_dict = {new_key: row_dict[key]
                           for key, new_key in self._COLUMN_TRANSLATION.items()}
            result.append(result_dict)
        return result

    def _iter_date_range(self):
        days_num = (self.end_date - self.start_date).days
        for i in range(days_num):
            yield self.start_date + timedelta(days=i)

    def iter_statistics(self):
        for date in self._iter_date_range():
            data = self._fetch_data_from_day(date)
            if data:
                yield from data
