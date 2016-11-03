# -*- coding: utf-8 -*-
import scrapy

from furl import furl


class CompanyItem(scrapy.Item):
    debut_date = scrapy.Field()
    total_actions = scrapy.Field()
    value = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    voivodship = scrapy.Field()
    isin = scrapy.Field()
    segment = scrapy.Field()
    sector = scrapy.Field()


class GPWCompaniesSpider(scrapy.Spider):
    name = "gpw_companies"
    _URL_TEMPLATE = 'https://www.gpw.pl/lista_spolek?search=1&query=&country=&voivodship='\
                    '&sector=&ph_tresc_glowna_offset={offset}'
    _COMPANY_INFO_URL_TEMPLATE = 'https://www.gpw.pl/ajaxindex.php?action=GPWListaSp&start=infoTab'\
                                 '&gls_isin={isin}&lang=PL'
    _COMPANY_INDICATORS_URL_TEMPLATE = 'https://www.gpw.pl/ajaxindex.php?action=GPWListaSp&start=indicatorsTab'\
                                       '&gls_isin={isin}&lang=PL'
    _COMPANY_URLS_SELECTOR = '//table[@class="tab02"]//tr/td[1]/a/@href'
    _COMPANY_ATTR_SELECTOR_TEMPLATE = '//*[text()="{selector_text}"]/following-sibling::td/text()'
    _COMPANY_ATTR_TO_SELECTOR_MAP = {
        'debut_date': 'Na giełdzie od:',
        'total_actions': 'Liczba wyemitowanych akcji',
        'value': 'Wartość rynkowa (mln zł)',
        'name': 'Nazwa:',
        'full_name': 'Nazwa pełna:',
        'voivodship': 'Województwo:',
        'segment': 'Rynek/Segment',
        'sector': 'Sektor'
    }
    _COMPANY_INFO_ATTRS = ['debut_date', 'name', 'full_name', 'voivodship']
    _COMPANY_INDICATORS_ATTRS = ['segment', 'sector', 'total_actions', 'value']

    def start_requests(self):
        request = scrapy.Request(self._URL_TEMPLATE.format(offset=0), callback=self.parse)
        request.meta['offset'] = 0
        yield request

    def _make_parse_company_request(self, company_url):
        isin = furl(company_url).path.segments[-2]
        assert isin, 'Invalid isin {}'.format(isin)
        company_info_tab_url = self._COMPANY_INFO_URL_TEMPLATE.format(isin=isin)
        request = scrapy.Request(company_info_tab_url, callback=self.parse_company_info_tab)
        request.meta['item'] = CompanyItem(isin=isin)
        yield request

    def parse(self, response):
        company_urls = response.xpath(self._COMPANY_URLS_SELECTOR).extract()
        for company_url in company_urls:
            yield from self._make_parse_company_request(company_url)
        companies_found = len(company_urls)
        if companies_found > 0:
            old_offset = response.meta['offset']
            new_offset = old_offset + companies_found
            request = scrapy.Request(self._URL_TEMPLATE.format(offset=new_offset), callback=self.parse)
            request.meta['offset'] = new_offset
            yield request

    def _extract_attribute(self, response, attr_name):
        selector_text = self._COMPANY_ATTR_TO_SELECTOR_MAP[attr_name]
        xpath_selector = self._COMPANY_ATTR_SELECTOR_TEMPLATE.format(selector_text=selector_text)
        values = scrapy.Selector(text=response.text).xpath(xpath_selector).extract()
        if len(values) == 1:
            value = values[0]
        else:
            value = None
        return value

    def parse_company_info_tab(self, response):
        item = response.meta['item']
        for attr_name in self._COMPANY_INFO_ATTRS:
            item[attr_name] = self._extract_attribute(response, attr_name)

        company_indicators_url = self._COMPANY_INDICATORS_URL_TEMPLATE.format(isin=item['isin'])
        request = scrapy.Request(company_indicators_url, callback=self.parse_company_indicators_data)
        request.meta['item'] = item
        yield request

    def parse_company_indicators_data(self, response):
        item = response.meta['item']
        for attr_name in self._COMPANY_INDICATORS_ATTRS:
            item[attr_name] = self._extract_attribute(response, attr_name)
        return item
