# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('chunks_chunk', 'content_ru', models.TextField(null=True))
        db.add_column('chunks_chunk', 'content_en', models.TextField(null=True))

    def backwards(self, orm):
        db.delete_column('chunks_chunk', 'content_ru')
        db.delete_column('chunks_chunk', 'content_en')

    models = dict()

    complete_apps = ['custom_admin']
