# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.management import BaseCommand
from scraper.utils import crawl_statistics


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_date = datetime(year=2014, month=1, day=1).date()
        crawl_statistics(start_date)
