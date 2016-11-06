FROM python:3.5

RUN pip install --upgrade pip
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ADD run_notebook.sh /run_notebook.sh

ENTRYPOINT ["/usr/bin/tini", "--"]