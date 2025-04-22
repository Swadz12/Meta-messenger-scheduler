@echo off
title Messenger Scheduler
color 0A
echo Running Messenger Scheduler

REM Go to directory where this .bat file is
cd /d "%~dp0"

REM Move one directory up, then go into code
cd ..
cd code

REM Run python script
python main.py

REM if error then stop
if errorlevel 1 pause
