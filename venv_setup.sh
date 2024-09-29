#!/bin/bash

# Check if the backend directory exists
backend_dir="backend"
if [ ! -d "backend_dir" ]; then
    echo "Creating backend service directory..."
    mkdir $backend_dir
fi

cd $backend_dir || exit

# Check if the virtual environment directory exists
venv_dir="venv"
if [ ! -d "$venv_dir" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $venv_dir
fi

# Activate the virtual environment
#source $venv_dir/bin/activate
source $venv_dir/Scripts/activate

# Check if requirements.txt exists and install dependencies
requirements_file="../requirements.txt"
if [ -f "$requirements_file" ]; then
    echo "Installing dependencies..."
    pip install -r $requirements_file
else
    echo "No requirements.txt found. Please make sure to install necessary packages manually."
fi

# Run the Django project initialization script
../DEVstart.sh
