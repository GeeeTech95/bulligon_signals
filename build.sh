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
python manage.py loaddata superuser.json


export DJANGO_SUPERUSER_EMAIL=admin1@bitcoinvoyager.finance
export DJANGO_SUPERUSER_PASSWORD=NRX6HbY.+dHA4s@

#python manage.py createsuperuser --no-input
