# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from scraper.run_crawler import crawl_companies


class Command(BaseCommand):

    def handle(self, *args, **options):
        crawl_companies()
