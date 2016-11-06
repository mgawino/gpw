#!/bin/bash

cd gpw
python setup.py develop
jupyter notebook --port=8888 --ip=0.0.0.0 --no-browser