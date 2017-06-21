#!/bin/sh
# shell script for resetting DB of users
# WARNING: DO NOT RUN SCRIPT ON SERVER

read -p "Are you sure? This will CLEAR the DB: " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python app/db/clean.py
	python app/db/make.py
fi
