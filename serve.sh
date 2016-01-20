#!/bin/bash

gunicorn -D -w8 --bind unix:/tmp/flask-pastebin.sock pastebin:app -p var/app.pid --access-logfile var/out.log --error-logfile var/error.log
