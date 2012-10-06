Требования
==========

Руками надо поставить: ``python2.6``, ``virtualenv``, ``sqlite3``.

Установка
=========

Получаем исходный код проекта::

    git clone git@github.com:RaD/meandre.git

Создаём и наполняем окружение
-----------------------------

Выполняем::

    virtualenv --no-site-packages env

    . ./env/bin/activate

    mkdir -p ./cache/pip

    ./env/bin/pip install --download-cache=./cache/pip/ -r ./reqs/base.txt
    ./env/bin/pip install --download-cache=./cache/pip/ -r ./reqs/dev.txt

Может потребоваться обновить локальное ПО:

    easy_install -U distribute

Дополнительное ПО
-----------------

Установка поискового движка::

    mkdir -p cache/haystack
    cd cache/haystack
    nice -n 19 bash ../../addon/xapian_install.sh
    cd -

Конфигурация проекта
--------------------

Изучите файл ``src/settings.py``. Необходимые правки выполните в файле
``src/settings_local.py``, который будет подгружаться при чтении
настроек проекта.

Подготовка базы данных
----------------------

Если планируется использовать MySQL, то надо создать базу:

    mysql -u root -p < ./addon/mysql_create_db.sql

По умолчанию, в качестве базы данных используется SQLite3::

    python manage.py syncdb --migrate --noinput

Если возникли ошибки, попробуйте::

    python manage.py syncdb --all
    python manage.py migrate --fake

Загружаем демонстрационные данные::

    echo "delete from django_content_type;" | python manage.py dbshell
    echo "delete from auth_permission;" | python manage.py dbshell
    python manage.py loaddata ./src/fixtures/demo_database.json

Дамп демонстрационной базы данных можно обновить так::

    python manage.py dumpdata --indent=2 --all > ./src/fixtures/demo_database.json


Запуск
------

При разработке мы пользуемся всей мощью ``devserver`` + ``werkzeug``::

    python manage.py runserver --werkzeug


Разработка
==========

Тестирование
------------

Тестирование должно проводится перед выполнением передачи набора коммитов в удалённый репозиторий.
Тестирование выполняется с помощью запуска одной из следующих команд::

    ./testing.sh APP_NAME
    ./testing.sh APP_NAME.CLASS_NAME.METHOD_NAME

База данных
-----------

Создание графической модели::

    python manage.py graph_models -e -a -g > models.dot
    dot -Tsvg models.dot > models.svg
    google-chrome models.svg

Миграции
--------

Новое приложение регистрируется так::

    python manage.py schemamigration APP_NAME --initial
    python manage.py migrate APP_NAME --fake 0001


Продуктив
=========

Создаём продуктивную конфигурацию в файле ``src/prod_settings.py``.

Синхронизируем проект на продуктив::

    ./deploy.sh


Виртуальное окружение
---------------------

Создаём окружение::

    mkdir -p ~/.local/lib/python2.6/site-packages

    easy_install-2.6 --prefix=~/.local virtualenv
    easy_install-2.6 --prefix=~/.local pip

    export PATH=~/.local/bin/:$PATH

Наполняем окружение::

    cd ${PATH_TO_SITE}

    virtualenv --python=python2.7 --no-site-packages env

    . ./env/bin/activate

    mkdir -p ~/cache/pip/
    ./env/bin/pip install --download-cache=~/cache/pip/ -r ./reqs/base.txt


Дополнительное ПО
-----------------

Установка поискового движка::

    mkdir -p ~/cache/haystack
    cd ~/cache/haystack
    nice -n 19 bash ../../${PATH_TO_SITE}/addon/xapian_install.sh
    cd -


Настройка Apache
----------------

Передаём управление сайтом Django::

    AddDefaultCharset utf-8
    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^\/static\/
    RewriteCond %{REQUEST_URI} !^\/media\/
    RewriteRule ^(.*)$ /webapp/$1 [L,QSA]


Настройка статики::

    cd ${PATH_TO_SITE}
    python manage.pyc collectstatic
    ln -s ~/site1/src/public/static/ ~/www/site1/public_html/static
    ln -s ~/site1/src/public/media/ ~/www/site1/public_html/media


База данных
-----------

Инициализация базы данных::

    python manage.pyc syncdb --migrate --noinput
    echo "delete from django_content_type;" | python manage.pyc dbshell
    echo "delete from auth_permission;" | python manage.pyc dbshell
    python manage.pyc dbshell
    \. DUMP.sql

Возможно понадобится имитация миграций для зависимостей::

    python manage.pyc migrate admin_tools.dashboard --fake
    python manage.pyc migrate admin_tools.menu --fake
    python manage.pyc migrate easy_thumbnails --fake


Запуск
------

Активируем сайт::

    cp ${PATH_TO_SITE}/src/wsgi.py ${PATH_TO_WWW}/webapp/webapp.wsgi


Сопровождение
=============

Обновление кода без рестарта сервиса::

    ./deploy.sh noapply

Обновление кода с рестартом сервиса::

    ./deploy.sh

Обновление кода с рестартом сервиса и обновлением статики::

    ./deploy.sh static

Обновление кода с рестартом сервиса и накатом миграций::

    ./deploy.sh migrate

Обновление кода с рестартом сервиса, накатом миграций и обновлением статики::

    ./deploy.sh migrate static
    ./deploy.sh static migrate

Note
====

Что бы не заморачиваться с настройкой поискового движка, добавьте в ``local_settings.py``::


    HAYSTACK_SEARCH_ENGINE = 'simple'
