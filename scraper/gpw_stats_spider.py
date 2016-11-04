# -*- coding: utf-8 -*-
import datetime

import scrapy
import xlrd


class StatisticsItem(scrapy.Item):
    date = scrapy.Field()
    name = scrapy.Field()
    isin = scrapy.Field()
    open_price = scrapy.Field()
    close_price = scrapy.Field()
    max_price = scrapy.Field()
    min_price = scrapy.Field()
    nominal_price = scrapy.Field()
    market_money = scrapy.Field()
    volume = scrapy.Field()
    open_positions = scrapy.Field()
    open_positions_value = scrapy.Field()
    change = scrapy.Field()
    currency = scrapy.Field()
    transactions_num = scrapy.Field()


class GPWStatisticsSpider(scrapy.Spider):
    _GPW_STATS_TEMPLATE = 'https://www.gpw.pl/notowania_archiwalne?type=10&date={date}&fetch.x=28&fetch.y=23'
    _DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, start_date, *args, **kwargs):
        super(GPWStatisticsSpider, self).__init__(*args, **kwargs)
        self.start_date = start_date

    def _make_request(self, date):
        start_date_str = date.strftime(self._DATE_FORMAT)
        request = scrapy.Request(self._GPW_STATS_TEMPLATE.format(date=start_date_str), callback=self.parse)
        request.meta['date'] = date
        return request

    def start_requests(self):
        yield self._make_request(self.start_date)

    def parse(self, response):
        date = response.meta['date']
        rows = XlsReader.parse_xls(response.body)
        yield from (StatisticsItem(**row) for row in rows)
        if date < datetime.datetime.now().date():
            yield self._make_request(date + datetime.timedelta(days=1))


class XlsReader:

    _COLUMN_TRANSLATION = {
        'Data': 'date',
        'Nazwa': 'name',
        'ISIN': 'isin',
        'Kurs otwarcia': 'open_price',
        'Kurs zamknięcia': 'close_price',
        'Kurs max': 'max_price',
        'Kurs min': 'min_price',
        'Cena nominalna': 'nominal_price',
        'Obrót': 'market_money',
        'Wolumen': 'volume',
        'Liczba otwartych pozycji': 'open_positions',
        'Wartość otwartych pozycji': 'open_positions_value',
        'Zmiana': 'change',
        'Waluta': 'currency',
        'Liczba Transakcji': 'transactions_num'
    }

    @staticmethod
    def parse_xls(file_contents):
        workbook = xlrd.open_workbook(file_contents=file_contents)
        sheet = workbook.sheet_by_index(0)
        rows = sheet.get_rows()
        try:
            header = next(rows)
        except StopIteration:
            return []
        header = [cell.value for cell in header]
        assert set(header) == set(XlsReader._COLUMN_TRANSLATION)
        result = []
        for row in rows:
            row_values = [cell.value for cell in row]
            assert len(row_values) == len(header)
            row_dict = dict(zip(header, row_values))
            result_dict = {new_key: row_dict[key]
                           for key, new_key in XlsReader._COLUMN_TRANSLATION.items()}
            result.append(result_dict)
        return result
