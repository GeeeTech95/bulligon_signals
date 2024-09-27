#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
python manage.py loaddata country.json
python manage.py loaddata plans.json


export DJANGO_SUPERUSER_EMAIL=admin@bullligonsignals.com
export DJANGO_SUPERUSER_PASSWORD=Y6li9p@Poko

python manage.py createsuperuser --no-input
