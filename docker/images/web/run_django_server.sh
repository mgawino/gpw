#!/bin/bash

cd gpw
python setup.py develop
cd gpw
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
