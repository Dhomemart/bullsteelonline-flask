@echo off
cd /d C:\flask_ultimate_project_fixed
start /min python app.py >> flask_log.txt 2>&1
