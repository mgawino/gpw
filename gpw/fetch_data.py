from collections import defaultdict

from datetime import timedelta, datetime

import ujson

import requests
import xlrd


GPW_URL_TEMPLATE = 'https://www.gpw.pl/notowania_archiwalne?type=10&date={date}&fetch.x=28&fetch.y=23'
RESULT_FILE = 'data.json'

# HEADER ['Data', 'Nazwa', 'ISIN', 'Waluta', 'Kurs otwarcia', 'Kurs max', 'Kurs min',
#         'Kurs zamknięcia', 'Zmiana', 'Wolumen', 'Liczba Transakcji', 'Obrót',
#         'Liczba otwartych pozycji', 'Wartość otwartych pozycji', 'Cena nominalna']

COLUMN_TRANSLATION = {
    'Data': 'date',
    'Nazwa': 'name',
    'Kurs otwarcia': 'open_price',
    'Kurs zamknięcia': 'close_price',
    'Kurs max': 'max_price',
    'Kurs min': 'min_price',
    'Cena nominalna': 'nominal_price',
    'Obrót': 'market_money',
    'Wolumen': 'volume',
    'Liczba otwartych pozycji': 'open_positions_num',
    'Wartość otwartych pozycji': 'open_positions_value',
    'Zmiana': 'changes',
    'Waluta': 'currency'
}


def _fetch_data_from_day(date):
    date_str = date.strftime("%Y-%m-%d")
    print('Fetching data from day {}'.format(date_str))
    gpw_url = GPW_URL_TEMPLATE.format(date=date_str)
    response = requests.get(gpw_url)
    response.raise_for_status()
    workbook = xlrd.open_workbook(file_contents=response.content)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.get_rows()
    try:
        header = next(rows)
    except StopIteration:
        print('Empty data')
        return {}
    header = [cell.value for cell in header]
    result = defaultdict(list)
    for row in rows:
        row_values = [cell.value for cell in row]
        row_dict = dict(zip(header, row_values))
        result_dict = {}
        for name, translation in COLUMN_TRANSLATION.items():
            result_dict[translation] = row_dict[name]
        company_name = result_dict.pop('name')
        result[company_name].append(result_dict)
    return result


def date_range(start_date, days_num):
    for i in range(days_num):
        yield start_date + timedelta(days=i)


def merge_dicts(first, second):
    for key, values in second.items():
        first[key].extend(values)
    return first


def fetch_data(start_date, days_num):
    result = defaultdict(list)
    for date in date_range(start_date, days_num):
        data = _fetch_data_from_day(date)
        result = merge_dicts(result, data)
    return result


if __name__ == '__main__':
    data = fetch_data(start_date=datetime(year=2016, month=1, day=1), days_num=200)
    with open(RESULT_FILE, 'w') as file:
        ujson.dump(data, file)
