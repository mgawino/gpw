from django.http import JsonResponse
from django.views.generic import TemplateView
from gpw.models import Company, Statistics


class IndexView(TemplateView):
    template_name = 'index.html'


def get_data(request, company_name, stats_name):
    isin = Company.objects.values('isin').filter(name=company_name).first()['isin']
    statistics = Statistics.objects.values(stats_name, 'date')\
        .filter(isin=isin).order_by('date').all()
    results = []
    for stats in statistics:
        results.append({'value': stats[stats_name], 'date': stats['date'].strftime("%Y-%m-%d")})
    return JsonResponse(dict(results=results))


def list_companies(request):
    company_names = Company.objects.values_list('name', flat=True).all()
    return JsonResponse(dict(company_names=list(company_names)))


def list_statistics(request):
    stat_names = [f.name for f in Statistics._meta.get_fields()
                  if f.name not in {'id', 'date', 'isin'}]
    return JsonResponse(dict(stat_names=stat_names))
