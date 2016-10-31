FROM python:3.5

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD entrypoint.sh /entrypoint.sh

EXPOSE 8000
