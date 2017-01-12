#!/bin/bash
source ../venv/bin/activate

echo "Setting environment variables"
mv ../.config.sh ../config.sh
source ../config.sh
mv ../config.sh ../.config.sh


echo "Starting server"
python ../main.py
