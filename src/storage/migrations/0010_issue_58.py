# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'Project.object_square'
        db.alter_column('storage_project', 'object_square', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):
        # Changing field 'Project.object_square'
        db.alter_column('storage_project', 'object_square', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2))
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'storage.companyteam': {
            'Meta': {'object_name': 'CompanyTeam'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'storage.customer': {
            'Meta': {'object_name': 'Customer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'customer_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Partner']", 'null': 'True', 'blank': 'True'}),
            'partnership_type': ('django.db.models.fields.IntegerField', [], {}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'workarea': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['storage.Workarea']", 'null': 'True', 'blank': 'True'})
        },
        'storage.financetransaction': {
            'Meta': {'object_name': 'FinanceTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'contract': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contractor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'done_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.FinanceTransaction']", 'null': 'True', 'blank': 'True'}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transaction_type': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_vat': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wallet': ('django.db.models.fields.IntegerField', [], {})
        },
        'storage.jobtype': {
            'Meta': {'object_name': 'JobType'},
            'css': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'storage.membership': {
            'Meta': {'object_name': 'Membership'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.CompanyTeam']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'leaved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Project']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.MembershipRole']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.CustomUser']", 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'Project'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'begin': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {}),
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
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '19', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stats': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.JobType']", 'symmetrical': 'False'}),
            'long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_name_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'long_name_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'made_for': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_square': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price_average': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'price_full': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'problems': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'productivity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '2'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'results_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'results_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '255', 'populate_from': "('short_name',)", 'recursive': 'False', 'blank': 'True'}),
            'staff': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.CustomUser']", 'through': "orm['storage.Membership']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'tasks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'storage.projectimage': {
            'Meta': {'object_name': 'ProjectImage'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'is_pro6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_teaser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Project']"})
        },
        'storage.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'storage.walletstate': {
            'Meta': {'object_name': 'WalletState'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.DateField', [], {}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'wallet': ('django.db.models.fields.IntegerField', [], {})
        },
        'storage.walletstatereport': {
            'Meta': {'object_name': 'WalletStateReport', 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'storage.workarea': {
            'Meta': {'object_name': 'Workarea'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'users.customuser': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'CustomUser', '_ormbases': ['auth.User']},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['storage']
