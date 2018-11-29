#!/bin/sh

cat <<EOF | python3 manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.filter(username="$apiUser").exists() or \
    User.objects.create_superuser("$apiUser", "$apiEmail", "$apiPassword")
EOF