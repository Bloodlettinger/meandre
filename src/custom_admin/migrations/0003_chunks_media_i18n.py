# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('chunks_media', 'media_ru', models.CharField(max_length=256, null=True, blank=True))
        db.add_column('chunks_media', 'media_en', models.CharField(max_length=256, null=True, blank=True))

    def backwards(self, orm):
        db.delete_column('chunks_media', 'media_ru')
        db.delete_column('chunks_media', 'media_en')

    models = dict()

    complete_apps = ['custom_admin']
