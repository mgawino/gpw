import ujson

from django.http import JsonResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


def get_data(request):
    with open('data.json') as file:
        data = ujson.load(file)
        return JsonResponse(data)


def list_companies(request):
    with open('data.json') as file:
        data = ujson.load(file)
        return JsonResponse(dict(companies=list(data.keys())))
