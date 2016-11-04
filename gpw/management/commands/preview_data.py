# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.db.models import Count
from gpw.models import Company


class Command(BaseCommand):

    def handle(self, *args, **options):
        sector_count = Company.objects.values('sector').annotate(count=Count('*'))
        for data in sector_count:
            print('{sector}: {count}'.format(**data))
