#!/bin/sh

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$apiUser', '$apiEmail', '$apiPassword')" | python3 manage.py shell