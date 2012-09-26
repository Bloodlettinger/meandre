# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('chunks_media', 'title_ru', models.CharField(max_length=64, null=True, blank=True))
        db.add_column('chunks_media', 'title_en', models.CharField(max_length=64, null=True, blank=True))
        db.add_column('chunks_media', 'desc_ru', models.CharField(max_length=256, null=True, blank=True))
        db.add_column('chunks_media', 'desc_en', models.CharField(max_length=256, null=True, blank=True))

    def backwards(self, orm):
        db.delete_column('chunks_media', 'title_ru')
        db.delete_column('chunks_media', 'title_en')
        db.delete_column('chunks_media', 'desc_ru')
        db.delete_column('chunks_media', 'desc_en')

    models = dict()

    complete_apps = ['custom_admin']
