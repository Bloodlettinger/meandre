Требования
==========

virtualenv, sqlite3

Установка
=========

git clone REPO

Создаём и наполняем окружение
-----------------------------

    virtualenv --python=python2.6 --system-site-packages env    # начиная с версии 1.7
    virtualenv --python=python2.6 env                           # до версии 1.7

    ./env/bin/pip install -E ./env -r ./reqs/base.txt
    ./env/bin/pip install -E ./env -r ./reqs/dev.txt
    . ./env/bin/activate

Конфигурация проекта
--------------------

Изучите файл ``src/settings.py``. Необходимые правки выполните в файле
``src/settings_local.py``, который будет подгружаться при чтении
настроек проекта.

Подготовка базы данных
----------------------

По умолчанию, в качестве базы данных используется SQLite3:

    python manage.py syncdb --migrate --noinput
    echo "delete from django_content_type;" | python manage.py dbshell
    echo "delete from auth_permission;" | python manage.py dbshell
    python manage.py loaddata ./src/fixtures/demo_database.json

Дамп демонстрационной базы данных можно обновить так:

    python manage.py dumpdata --indent=2 --all > ./src/fixtures/demo_database.json


Запуск
------

При разработке мы пользуемся всей мощью devserver + werkzeug:

    python manage.py runserver --werkzeug


Тестирование
============

Тестирование должно проводится перед выполнением передачи набора коммитов в удалённый репозиторий. Тестирование выполняется с помощью запуска следующих команд в каталоге `src`::

  python manage.py test storage
  # python manage.py test api

Схема базы данных
=================

Создание графической модели:

    python manage.py graph_models -e -a -g > models.dot
    dot -Tsvg models.dot > models.svg
    google-chrome models.svg
