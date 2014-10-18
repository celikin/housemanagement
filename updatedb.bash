#!/usr/bin/bash
set -x
./manage.py makemigrations &&
	./manage.py migrate &&
	./manage.py loaddata initial companies arbitrary