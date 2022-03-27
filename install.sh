#!/bin/bash

set -e

PACKAGE_ROOT=$(cd $(dirname $0); pwd)

if [[ !(-d venv) ]]
then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip

cd ${PACKAGE_ROOT}
pip install -r requirements.txt
pip install -e .
