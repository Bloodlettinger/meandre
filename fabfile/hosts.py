# -*- coding: utf-8 -*-

from fab_deploy import *
from src import local_settings as settings


@define_host(settings.SERVER_URL)
def production():
    return dict(
        WSGI=settings.PROD_WSGI,
        ENV_DIR=settings.PROD_ENV_DIR,
        PROJECT_DIR=settings.PROD_HOST_DIR,
        DB_HOST=settings.PROD_DB_HOST,
        DB_NAME=settings.PROD_DB_NAME,
        DB_USER=settings.PROD_DB_USER,
        DB_PASS=settings.PROD_DB_PASS,
        MIGRATE_DUMP=settings.PROD_MIGRATE_DUMP
    )


@define_host(settings.SERVER_URL)
def testing():
    return dict(
        WSGI=settings.TEST_WSGI,
        ENV_DIR=settings.TEST_ENV_DIR,
        PROJECT_DIR=settings.TEST_HOST_DIR,
        DB_HOST=settings.TEST_DB_HOST,
        DB_NAME=settings.TEST_DB_NAME,
        DB_USER=settings.TEST_DB_USER,
        DB_PASS=settings.TEST_DB_PASS,
        MIGRATE_DUMP=settings.TEST_MIGRATE_DUMP
    )
