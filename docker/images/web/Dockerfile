FROM python:3.5

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD run_django_server.sh /run_django_server.sh

EXPOSE 8000
