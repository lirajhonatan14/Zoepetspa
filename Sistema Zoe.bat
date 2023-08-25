@ECHO off
cd "C:\Users\liraj\Documents\Sistema Zoe"
call venv\Scripts\activate
start "" http:127.0.0.1:8000
python manage.py runserver
PAUSE
