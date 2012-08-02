#!/bin/bash

# Скрипт предназначен для сбора из исходного кода и шаблонов текстовых
# строк, предназначенных для перевода.

LANGUAGES="ru"
PROJECTS="src"
APPS="custom_admin frontend storage uploader users"

if test $# -gt 0; then
    APPS=$@
fi

for lang in ${LANGUAGES}; do
    for project in ${PROJECTS}; do
        for app in ${APPS}; do
            if test -d ${project}/${app}; then
                cd ${project}/${app}
                echo "Update messages for application: ${project}.${app}"
                mkdir -p locale
                django-admin.py makemessages --locale ${lang}
                cd -
            else
                echo "Unknown application ${app}. Skipping..."
            fi
        done
    done
done

exit 0
