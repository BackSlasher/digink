#!/bin/bash

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")"
virtualenv venv --system-site-packages
venv/bin/python -m pip install -r requirements.txt
