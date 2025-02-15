#!/bin/bash

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual muhit aktivlashtirildi"
fi

if [ -d "usersapp/migrations" ]; then
    rm -rf usersapp/migrations/*
    echo "Usersapp migrations tozalandi"
fi

if [ -d "cardapp/migrations" ]; then
    rm -rf cardapp/migrations/*
    echo "Cardapp migrations tozalandi"
fi

touch usersapp/migrations/__init__.py
touch cardapp/migrations/__init__.py
echo "Yangi __init__.py fayllari yaratildi"

python manage.py collectstatic --noinput

python manage.py makemigrations usersapp
python manage.py makemigrations cardapp
python manage.py migrate
python manage.py runserver