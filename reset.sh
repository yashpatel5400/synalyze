#!/bin/sh
# shell script for resetting DB of users
# WARNING: DO NOT RUN SCRIPT ON SERVER

python app/db/clean.py
python app/db/make.py
