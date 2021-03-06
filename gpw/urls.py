"""gpw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from gpw.views import IndexView, get_data, list_companies, list_statistics

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', IndexView.as_view()),
    url(r'^data/(?P<company_name>.*)/(?P<stats_name>.*)/$', get_data),
    url(r'^company_names/', list_companies),
    url(r'^stat_names/', list_statistics)
]
