# -*- coding: utf-8 -*-
import logging

from scraper.gpw_company_spider import GPWCompaniesSpider
from scraper.gpw_stats_spider import GPWStatisticsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

USER_AGENT = 'Mozilla/4.0 AppleWebKit/437.36 (KHTML, like Gecko) Chrome/50.0.2704.106 Safari/507.36'


def crawl_companies():
    settings = get_project_settings()
    settings['USER_AGENT'] = USER_AGENT
    settings['ITEM_PIPELINES'] = {'scraper.pipelines.CompanyPipeline': 1}
    settings['LOG_LEVEL'] = logging.INFO
    process = CrawlerProcess(settings)
    process.crawl(GPWCompaniesSpider, name='gpw_companies')
    process.start()


def crawl_statistics(start_date):
    settings = get_project_settings()
    settings['USER_AGENT'] = USER_AGENT
    settings['ITEM_PIPELINES'] = {'scraper.pipelines.StatisticsPipeline': 1}
    settings['LOG_LEVEL'] = logging.INFO
    process = CrawlerProcess(settings)
    process.crawl(GPWStatisticsSpider, start_date, name='gpw_statistics')
    process.start()
