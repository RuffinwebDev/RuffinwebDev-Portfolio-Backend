@echo off

:: Check if the virtual environment directory exists
set venv_dir=venv
if not exist %venv_dir% (
    echo Creating virtual environment...
    python -m venv %venv_dir%
)

:: Activate the virtual environment
call %venv_dir%\Scripts\activate

:: Check if requirements.txt exists and install dependencies
set requirements_file=requirements.txt
if exist %requirements_file% (
    echo Installing dependencies...
    pip install -r %requirements_file% --user
) else (
    echo No requirements.txt found. Please make sure to install necessary packages manually.
)

:: Run the Django project initialization script
call DEVstart.sh
