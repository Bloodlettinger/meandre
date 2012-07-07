#!/bin/bash

# Скрипт предназначен для сбора из исходного кода и шаблонов текстовых
# строк, предназначенных для перевода.

LANGUAGES="ru"
PROJECTS="src"
APPS="frontend storage uploader users"

for lang in ${LANGUAGES}; do
    for project in ${PROJECTS}; do
        for app in ${APPS}; do
            cd ${project}/${app}
            echo "Update messages for application: ${project}.${app}"
            mkdir -p locale
            django-admin.py makemessages --locale ${lang}
            cd -
        done
    done
done

exit 0
