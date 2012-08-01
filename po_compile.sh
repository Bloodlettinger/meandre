#!/bin/bash

# Скрипт предназначен для компиляции переводов.

PROJECTS="src"
APPS="custom_admin frontend storage uploader users"

for project in ${PROJECTS}; do
    for app in ${APPS}; do
        cd ${project}/${app}
        echo "Compile messages for application: ${project}.${app}"
        django-admin.py compilemessages
        cd -
    done
done

exit 0
