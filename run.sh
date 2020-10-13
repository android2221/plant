#!/bin/bash
cd /home/pi/projects/plant
source ./env/bin/activate
pip install -r requirements.txt
python ./watering.py