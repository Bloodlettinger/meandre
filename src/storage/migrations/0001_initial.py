# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Workarea'
        db.create_table('storage_workarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('storage', ['Workarea'])

        # Adding model 'Partner'
        db.create_table('storage_partner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765)),
        ))
        db.send_create_signal('storage', ['Partner'])

        # Adding model 'Customer'
        db.create_table('storage_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Partner'], null=True, blank=True)),
            ('customer_type', self.gf('django.db.models.fields.IntegerField')()),
            ('partnership_type', self.gf('django.db.models.fields.IntegerField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('long_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('storage', ['Customer'])

        # Adding M2M table for field workarea on 'Customer'
        db.create_table('storage_customer_workarea', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customer', models.ForeignKey(orm['storage.customer'], null=False)),
            ('workarea', models.ForeignKey(orm['storage.workarea'], null=False))
        ))
        db.create_unique('storage_customer_workarea', ['customer_id', 'workarea_id'])

        # Adding model 'CompanyTeam'
        db.create_table('storage_companyteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('storage', ['CompanyTeam'])

        # Adding model 'JobType'
        db.create_table('storage_jobtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('css', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('long_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('storage', ['JobType'])

        # Adding model 'Project'
        db.create_table('storage_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Customer'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_name_ru', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('long_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_name_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_name_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ptype', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('desc_short', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_short_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_short_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_long', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_long_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_long_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tasks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tasks_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tasks_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('problems', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('problems_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('problems_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('results', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('results_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('results_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('made_for', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('object_square', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=4)),
            ('duration_production', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_changes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_discussion', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_other', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('begin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('price_full', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=4)),
            ('currency', self.gf('django.db.models.fields.IntegerField')()),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=19, decimal_places=4)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_stats', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('productivity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=4)),
            ('price_average', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=4)),
            ('slug', self.gf('django_autoslug.fields.AutoSlugField')(unique=True, max_length=255, populate_from=('short_name',), recursive=False, blank=True)),
        ))
        db.send_create_signal('storage', ['Project'])

        # Adding M2M table for field job_type on 'Project'
        db.create_table('storage_project_job_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['storage.project'], null=False)),
            ('jobtype', models.ForeignKey(orm['storage.jobtype'], null=False))
        ))
        db.create_unique('storage_project_job_type', ['project_id', 'jobtype_id'])

        # Adding model 'Membership'
        db.create_table('storage_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'], null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.CompanyTeam'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('joined_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('leaved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['Membership'])

        # Adding M2M table for field role on 'Membership'
        db.create_table('storage_membership_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm['storage.membership'], null=False)),
            ('customgroup', models.ForeignKey(orm['users.customgroup'], null=False))
        ))
        db.create_unique('storage_membership_role', ['membership_id', 'customgroup_id'])

        # Adding model 'ProjectImage'
        db.create_table('storage_projectimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Project'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_teaser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_pro6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('storage', ['ProjectImage'])

        # Adding model 'FinanceTransaction'
        db.create_table('storage_financetransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.FinanceTransaction'], null=True, blank=True)),
            ('wallet', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=4)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('transaction_type', self.gf('django.db.models.fields.IntegerField')()),
            ('transaction_vat', self.gf('django.db.models.fields.IntegerField')()),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=4, blank=True)),
            ('contract', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('contractor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('done_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('storage', ['FinanceTransaction'])

        # Adding model 'WalletState'
        db.create_table('storage_walletstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=4)),
            ('moment', self.gf('django.db.models.fields.DateField')()),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('storage', ['WalletState'])

        # Adding model 'Recommendation'
        db.create_table('storage_recommendation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('storage', ['Recommendation'])

    def backwards(self, orm):
        # Deleting model 'Workarea'
        db.delete_table('storage_workarea')

        # Deleting model 'Partner'
        db.delete_table('storage_partner')

        # Deleting model 'Customer'
        db.delete_table('storage_customer')

        # Removing M2M table for field workarea on 'Customer'
        db.delete_table('storage_customer_workarea')

        # Deleting model 'CompanyTeam'
        db.delete_table('storage_companyteam')

        # Deleting model 'JobType'
        db.delete_table('storage_jobtype')

        # Deleting model 'Project'
        db.delete_table('storage_project')

        # Removing M2M table for field job_type on 'Project'
        db.delete_table('storage_project_job_type')

        # Deleting model 'Membership'
        db.delete_table('storage_membership')

        # Removing M2M table for field role on 'Membership'
        db.delete_table('storage_membership_role')

        # Deleting model 'ProjectImage'
        db.delete_table('storage_projectimage')

        # Deleting model 'FinanceTransaction'
        db.delete_table('storage_financetransaction')

        # Deleting model 'WalletState'
        db.delete_table('storage_walletstate')

        # Deleting model 'Recommendation'
        db.delete_table('storage_recommendation')

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
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '4'}),
            'contract': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contractor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'done_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '4', 'blank': 'True'}),
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
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.CustomUser']", 'null': 'True', 'blank': 'True'})
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
            'exchange_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '19', 'decimal_places': '4'}),
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
            'object_square': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '4'}),
            'price_average': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '4'}),
            'price_full': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '4'}),
            'problems': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'problems_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'productivity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '19', 'decimal_places': '4'}),
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
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '4'}),
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