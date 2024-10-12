#!/bin/bash

# Ensure the script is running in the virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate your virtual environment first."
    exit 1
fi

echo "current directory: $PWD"
# Navigate to the backend directory
#cd backend || exit

# Function to create a new Django app if it doesn't exist
create_app() {
    app_name=$1
    if [ ! -d "$project_dir/$app_name" ]; then
        echo "Creating Django app: $app_name"
        python3 manage.py startapp $app_name
    else
        echo "App $app_name already exists."
    fi
}

echo "current directory: $PWD"

# Function to prompt for input or read from config file
read_config() {
    if [ -f "$config_file" ]; then
        source $config_file
    else
        read -p "Enter project directory: " project_dir
        read -p "Enter apps to create (space-separated): " apps
    fi
}

# Load configuration or prompt user
config_file="./project_init_config.sh"
read_config

# Create project directory if it doesn't exist
mkdir -p $project_dir
cd $project_dir

# Initialize Django project if not already initialized
if [ ! -f "manage.py" ]; then
    echo "Initializing new Django project..."
    django-admin startproject backend .
fi

# Create the necessary Django apps
for app in $apps; do
    if [ "$app" != "auth" ]; then
        create_app $app
    fi
done

# Add the apps to the INSTALLED_APPS in settings.py
for app in $apps; do
    if [ "$app" != "auth" ] && ! grep -q "'$app'," backend/settings.py; then
        sed -i "/INSTALLED_APPS = \[/ a\    '$app'," backend/settings.py
        echo "Added $app to INSTALLED_APPS"
    fi
done

# Make and apply migrations
echo "Making and applying migrations..."
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations backend
python3 manage.py migrate backend


for app in $apps; do
    python3 manage.py migrate $app
done

echo "Django project setup complete."

# Optionally start Docker containers
# docker-compose up -d
# sleep 10
# docker-compose exec web python manage.py import_videos /app/output
# docker-compose logs -f


# Email sending functionality is now handled the backend alone.