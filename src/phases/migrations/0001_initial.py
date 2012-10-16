# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Phase'
        db.create_table('phases_phase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('phases', ['Phase'])

        # Adding model 'Step'
        db.create_table('phases_step', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phases.Phase'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('times', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('phases', ['Step'])

        # Adding model 'Relation'
        db.create_table('phases_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Project'])),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phases.Step'])),
            ('duration_a', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('duration_b', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cost', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('phases', ['Relation'])

    def backwards(self, orm):
        # Deleting model 'Phase'
        db.delete_table('phases_phase')

        # Deleting model 'Step'
        db.delete_table('phases_step')

        # Deleting model 'Relation'
        db.delete_table('phases_relation')

    models = {
        'phases.phase': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Phase'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'phases.relation': {
            'Meta': {'object_name': 'Relation'},
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'duration_a': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'duration_b': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Project']"}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phases.Step']"})
        },
        'phases.step': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Step'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phases.Phase']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'times': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'storage.customer': {
            'Meta': {'object_name': 'Customer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'customer_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_name_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_name_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Partner']", 'null': 'True', 'blank': 'True'}),
            'partnership_type': ('django.db.models.fields.IntegerField', [], {}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'workarea': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['storage.Workarea']", 'null': 'True', 'blank': 'True'})
        },
        'storage.jobtype': {
            'Meta': {'object_name': 'JobType'},
            'css': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'duration_en': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'duration_ru': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'long_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'long_title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'storage.membership': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'leaved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.MembershipRole']"}),
            'staff': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.Staff']", 'symmetrical': 'False'})
        },
        'storage.membershiprole': {
            'Meta': {'object_name': 'MembershipRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'storage.partner': {
            'Meta': {'object_name': 'Partner'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'storage.project': {
            'Meta': {'ordering': "('-reg_date',)", 'object_name': 'Project'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Customer']"}),
            'desc_long': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_long_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_long_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_short': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_short_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_short_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration_changes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'duration_discussion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'duration_other': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'duration_production': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '19', 'decimal_places': '2'}),
            'finished_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stats': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public_ru': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['storage.JobType']", 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'long_name_en': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'long_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'made_for': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_square': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price_average': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'price_full': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'problems': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'productivity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'reg_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'results_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'results_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "('short_name',)", 'recursive': 'False', 'blank': 'True'}),
            'staff_roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.MembershipRole']", 'through': "orm['storage.Membership']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tasks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'storage.staff': {
            'Meta': {'object_name': 'Staff'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'address_ru': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'company_en': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'company_ru': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'first_name_en': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'first_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'last_name_en': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'last_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'which': ('django.db.models.fields.IntegerField', [], {})
        },
        'storage.workarea': {
            'Meta': {'object_name': 'Workarea'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        }
    }

    complete_apps = ['phases']
