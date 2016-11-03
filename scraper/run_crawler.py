# -*- coding: utf-8 -*-
import logging

from scraper.gpw_company_spider import GPWCompaniesSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def crawl_companies():
    settings = get_project_settings()
    settings['USER_AGENT'] = 'Mozilla/4.0 AppleWebKit/437.36 (KHTML, like Gecko) Chrome/50.0.2704.106 Safari/507.36'
    settings['ITEM_PIPELINES'] = {'scraper.company_pipeline.CompanyPipeline': 1}
    settings['LOG_LEVEL'] = logging.INFO
    process = CrawlerProcess(settings)
    process.crawl(GPWCompaniesSpider())
    process.start()