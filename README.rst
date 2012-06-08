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

По умолчанию, в качестве базы данных используется SQLite3::

    python manage.py syncdb --migrate --noinput
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
Тестирование выполняется с помощью запуска следующих команд в каталоге `src`::

    python manage.py test storage
    # python manage.py test api

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

    virtualenv --python=python2.6 --system-site-packages env    # начиная с версии 1.7
    virtualenv --python=python2.6 env                           # до версии 1.7

    ./env/bin/pip install -r ./reqs/base.txt


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


Дополнительное ПО
-----------------

Установка поискового движка::

    cd ~/tmp
    nice -n 19 bash ${PATH_TO_SITE}/addon/xapian_install.sh
    rm -rf ./xapian*
    cd -


База данных
-----------

Инициализация базы данных::

    python manage.py syncdb --migrate --noinput
    echo "delete from django_content_type;" | python manage.pyc dbshell
    echo "delete from auth_permission;" | python manage.pyc dbshell
    python manage.pyc dbshell
    \. DUMP.sql


Запуск
------

Активируем сайт::

    cp ${PATH_TO_SITE}/src/wsgi.py ${PATH_TO_WWW}/webapp/webapp.wsgi
