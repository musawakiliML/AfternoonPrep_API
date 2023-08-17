#!/bin/bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
source env/bin/activate
python3 main.py