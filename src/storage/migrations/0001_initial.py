# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

from south.db import db
from south.v2 import SchemaMigration


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
            ('short_name_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('long_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_name_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_name_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
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

        # Adding model 'JobType'
        db.create_table('storage_jobtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('css', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('short_title_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('long_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('long_title_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('long_title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('description_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('storage', ['JobType'])

        # Adding model 'Project'
        db.create_table('storage_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Customer'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_ru', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('short_name_ru', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('long_name_ru', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('long_name_en', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('ptype', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
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
            ('object_square', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_production', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_changes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_discussion', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duration_other', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('begin', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('price_full', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(default=1.0, max_digits=19, decimal_places=2)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_stats', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reg_date', self.gf('django.db.models.fields.DateField')(default=timezone.now)),
            ('productivity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=2)),
            ('price_average', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=19, decimal_places=2)),
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

        # Adding model 'Staff'
        db.create_table('storage_staff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('which', self.gf('django.db.models.fields.IntegerField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['Staff'])

        # Adding model 'StaffPerson'
        db.create_table('storage_staffperson', (
            ('staff_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['storage.Staff'], unique=True, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['StaffPerson'])

        # Adding model 'StaffCompany'
        db.create_table('storage_staffcompany', (
            ('staff_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['storage.Staff'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('storage', ['StaffCompany'])

        # Adding model 'MembershipRole'
        db.create_table('storage_membershiprole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['MembershipRole'])

        # Adding model 'Membership'
        db.create_table('storage_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('joined_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('leaved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['Membership'])

        # Adding M2M table for field role on 'Membership'
        db.create_table('storage_membership_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm['storage.membership'], null=False)),
            ('membershiprole', models.ForeignKey(orm['storage.membershiprole'], null=False))
        ))
        db.create_unique('storage_membership_role', ['membership_id', 'membershiprole_id'])

        # Adding model 'MembershipStaff'
        db.create_table('storage_membershipstaff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Project'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Staff'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('joined_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('leaved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('storage', ['MembershipStaff'])

        # Adding M2M table for field role on 'MembershipStaff'
        db.create_table('storage_membershipstaff_role', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membershipstaff', models.ForeignKey(orm['storage.membershipstaff'], null=False)),
            ('membershiprole', models.ForeignKey(orm['storage.membershiprole'], null=False))
        ))
        db.create_unique('storage_membershipstaff_role', ['membershipstaff_id', 'membershiprole_id'])

        # Adding model 'FinanceTransaction'
        db.create_table('storage_financetransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.FinanceTransaction'], null=True, blank=True)),
            ('wallet', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('transaction_type', self.gf('django.db.models.fields.IntegerField')()),
            ('transaction_vat', self.gf('django.db.models.fields.IntegerField')()),
            ('exchange_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=2, blank=True)),
            ('contract', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('contractor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('done_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('storage', ['FinanceTransaction'])

        # Adding model 'WalletState'
        db.create_table('storage_walletstate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wallet', self.gf('django.db.models.fields.IntegerField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=19, decimal_places=2)),
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

        # Deleting model 'JobType'
        db.delete_table('storage_jobtype')

        # Deleting model 'Project'
        db.delete_table('storage_project')

        # Removing M2M table for field job_type on 'Project'
        db.delete_table('storage_project_job_type')

        # Deleting model 'Staff'
        db.delete_table('storage_staff')

        # Deleting model 'StaffPerson'
        db.delete_table('storage_staffperson')

        # Deleting model 'StaffCompany'
        db.delete_table('storage_staffcompany')

        # Deleting model 'MembershipRole'
        db.delete_table('storage_membershiprole')

        # Deleting model 'Membership'
        db.delete_table('storage_membership')

        # Removing M2M table for field role on 'Membership'
        db.delete_table('storage_membership_role')

        # Deleting model 'MembershipStaff'
        db.delete_table('storage_membershipstaff')

        # Removing M2M table for field role on 'MembershipStaff'
        db.delete_table('storage_membershipstaff_role')

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
        'storage.financetransaction': {
            'Meta': {'object_name': 'FinanceTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'contract': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contractor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'done_at': ('django.db.models.fields.DateTimeField', [], {}),
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
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'long_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'long_title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'storage.membership': {
            'Meta': {'object_name': 'Membership'},
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
        'storage.membershipstaff': {
            'Meta': {'ordering': "('position',)", 'object_name': 'MembershipStaff'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'leaved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Project']"}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.MembershipRole']", 'symmetrical': 'False'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['storage.Staff']"})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_stats': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['storage.JobType']", 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'long_name_en': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'long_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'made_for': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_square': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'staff': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['users.CustomUser']", 'through': "orm['storage.Membership']", 'symmetrical': 'False'}),
            'staff_new': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['storage.Staff']", 'through': "orm['storage.MembershipStaff']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tasks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tasks_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'storage.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'storage.staff': {
            'Meta': {'object_name': 'Staff'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'which': ('django.db.models.fields.IntegerField', [], {})
        },
        'storage.staffcompany': {
            'Meta': {'object_name': 'StaffCompany', '_ormbases': ['storage.Staff']},
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'staff_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['storage.Staff']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'storage.staffperson': {
            'Meta': {'object_name': 'StaffPerson', '_ormbases': ['storage.Staff']},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'staff_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['storage.Staff']", 'unique': 'True', 'primary_key': 'True'})
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
        'users.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'users.customuser': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'CustomUser', '_ormbases': ['auth.User']},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Company']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['storage']
