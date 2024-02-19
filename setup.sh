#!/usr/bin/bash

# create a virtual environment for the project
python -m venv env
# activate env
source ./env/bin/activate
# install requirements
python -m pip install requirements.txt
# close venv
source deactivate