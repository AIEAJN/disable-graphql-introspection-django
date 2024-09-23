#!/bin/bash

set -e

# Fonction pour exécuter les migrations
run_migrations() {
    echo "Running migrations..."
    poetry run python /app/api/manage.py collectstatic --noinput
    poetry run python /app/api/manage.py makemigrations
    poetry run python /app/api/manage.py migrate

}

run_scripts() {
    echo "Running scripts..."
    poetry run python /app/automation/scripts_executor.py
}
# Fonction pour démarrer Gunicorn
start_gunicorn() {
    echo "Starting Gunicorn..."
    cd /app/api
    # poetry run python manage.py runserver 8000 
    poetry run gunicorn api.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 
}

# Vérifier si le fichier pyproject.toml a changé
if [ -f /app/pyproject.toml ]; then
    if [ ! -f /app/.pyproject.toml.md5 ] || [ "$(md5sum /app/pyproject.toml | awk '{ print $1 }')" != "$(cat /app/.pyproject.toml.md5)" ]; then
        echo "pyproject.toml has changed. Running poetry install..."
        poetry lock --no-update
        poetry install
        md5sum /app/pyproject.toml | awk '{ print $1 }' > /app/.pyproject.toml.md5
    else
        echo "pyproject.toml has not changed. Skipping poetry install."
    fi
fi

# Exécuter les migrations
run_migrations

# Exécuter les scripts
run_scripts

# Démarrer Gunicorn
start_gunicorn
