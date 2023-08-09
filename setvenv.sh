#!/bin/sh

if [ ! -d "venv" ];
    then python3.11 -m venv venv;
fi

source venv/bin/activate;
pip install --upgrade pip;
pip install -r backend/dev.requirements.txt;
pre-commit install;
