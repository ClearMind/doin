# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SettlementType'
        db.create_table('attestation_settlementtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('abbreviate', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
        ))
        db.send_create_signal('attestation', ['SettlementType'])

        # Adding model 'Settlement'
        db.create_table('attestation_settlement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.SettlementType'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('attestation', ['Settlement'])

        # Adding model 'Territory'
        db.create_table('attestation_territory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal('attestation', ['Territory'])

        # Adding model 'Post'
        db.create_table('attestation_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('attestation', ['Post'])

        # Adding model 'PostInCommission'
        db.create_table('attestation_postincommission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('is_chairman', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_vicechairman', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('attestation', ['PostInCommission'])

        # Adding model 'Organization'
        db.create_table('attestation_organization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('settlement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Settlement'])),
            ('abbreviate', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('attestation', ['Organization'])

        # Adding model 'CertifyingCommissionMember'
        db.create_table('attestation_certifyingcommissionmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('post_in_commission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.PostInCommission'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Post'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Organization'])),
        ))
        db.send_create_signal('attestation', ['CertifyingCommissionMember'])

        # Adding model 'CertifyingCommission'
        db.create_table('attestation_certifyingcommission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('attestation', ['CertifyingCommission'])

        # Adding M2M table for field members on 'CertifyingCommission'
        db.create_table('attestation_certifyingcommission_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('certifyingcommission', models.ForeignKey(orm['attestation.certifyingcommission'], null=False)),
            ('certifyingcommissionmember', models.ForeignKey(orm['attestation.certifyingcommissionmember'], null=False))
        ))
        db.create_unique('attestation_certifyingcommission_members', ['certifyingcommission_id', 'certifyingcommissionmember_id'])

        # Adding model 'Expert'
        db.create_table('attestation_expert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Post'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Organization'])),
        ))
        db.send_create_signal('attestation', ['Expert'])

        # Adding model 'ExpertCommission'
        db.create_table('attestation_expertcommission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateField')()),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('attestation', ['ExpertCommission'])

        # Adding M2M table for field members on 'ExpertCommission'
        db.create_table('attestation_expertcommission_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('expertcommission', models.ForeignKey(orm['attestation.expertcommission'], null=False)),
            ('expert', models.ForeignKey(orm['attestation.expert'], null=False))
        ))
        db.create_unique('attestation_expertcommission_members', ['expertcommission_id', 'expert_id'])

        # Adding model 'Administrator'
        db.create_table('attestation_administrator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Post'])),
        ))
        db.send_create_signal('attestation', ['Administrator'])

        # Adding model 'Qualification'
        db.create_table('attestation_qualification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('request_form', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('for_confirmation', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('attestation', ['Qualification'])

        # Adding model 'Degree'
        db.create_table('attestation_degree', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('attestation', ['Degree'])

        # Adding model 'AcademicTitle'
        db.create_table('attestation_academictitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('attestation', ['AcademicTitle'])

        # Adding model 'Title'
        db.create_table('attestation_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('attestation', ['Title'])

        # Adding model 'RequestStatus'
        db.create_table('attestation_requeststatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_rejected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_docs_received', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_in_expertise', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('attestation', ['RequestStatus'])

        # Adding model 'Request'
        db.create_table('attestation_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Post'])),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Territory'], null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Organization'], null=True, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Qualification'])),
            ('with_qualification', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='request_has_set', null=True, to=orm['attestation.Qualification'])),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('results', self.gf('django.db.models.fields.TextField')()),
            ('experience', self.gf('django.db.models.fields.IntegerField')()),
            ('pedagogical_experience', self.gf('django.db.models.fields.IntegerField')()),
            ('post_experience', self.gf('django.db.models.fields.IntegerField')()),
            ('organization_experience', self.gf('django.db.models.fields.IntegerField')()),
            ('degree', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Degree'], null=True, blank=True)),
            ('academic_title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.AcademicTitle'], null=True, blank=True)),
            ('presence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('trainings', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal('attestation', ['Request'])

        # Adding M2M table for field experts on 'Request'
        db.create_table('attestation_request_experts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm['attestation.request'], null=False)),
            ('expert', models.ForeignKey(orm['attestation.expert'], null=False))
        ))
        db.create_unique('attestation_request_experts', ['request_id', 'expert_id'])

        # Adding model 'Education'
        db.create_table('attestation_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('diploma_year', self.gf('django.db.models.fields.IntegerField')()),
            ('speciality', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('qualification', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Request'])),
        ))
        db.send_create_signal('attestation', ['Education'])

        # Adding model 'RequestFlow'
        db.create_table('attestation_requestflow', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Request'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.RequestStatus'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('attestation', ['RequestFlow'])


    def backwards(self, orm):
        # Deleting model 'SettlementType'
        db.delete_table('attestation_settlementtype')

        # Deleting model 'Settlement'
        db.delete_table('attestation_settlement')

        # Deleting model 'Territory'
        db.delete_table('attestation_territory')

        # Deleting model 'Post'
        db.delete_table('attestation_post')

        # Deleting model 'PostInCommission'
        db.delete_table('attestation_postincommission')

        # Deleting model 'Organization'
        db.delete_table('attestation_organization')

        # Deleting model 'CertifyingCommissionMember'
        db.delete_table('attestation_certifyingcommissionmember')

        # Deleting model 'CertifyingCommission'
        db.delete_table('attestation_certifyingcommission')

        # Removing M2M table for field members on 'CertifyingCommission'
        db.delete_table('attestation_certifyingcommission_members')

        # Deleting model 'Expert'
        db.delete_table('attestation_expert')

        # Deleting model 'ExpertCommission'
        db.delete_table('attestation_expertcommission')

        # Removing M2M table for field members on 'ExpertCommission'
        db.delete_table('attestation_expertcommission_members')

        # Deleting model 'Administrator'
        db.delete_table('attestation_administrator')

        # Deleting model 'Qualification'
        db.delete_table('attestation_qualification')

        # Deleting model 'Degree'
        db.delete_table('attestation_degree')

        # Deleting model 'AcademicTitle'
        db.delete_table('attestation_academictitle')

        # Deleting model 'Title'
        db.delete_table('attestation_title')

        # Deleting model 'RequestStatus'
        db.delete_table('attestation_requeststatus')

        # Deleting model 'Request'
        db.delete_table('attestation_request')

        # Removing M2M table for field experts on 'Request'
        db.delete_table('attestation_request_experts')

        # Deleting model 'Education'
        db.delete_table('attestation_education')

        # Deleting model 'RequestFlow'
        db.delete_table('attestation_requestflow')


    models = {
        'attestation.academictitle': {
            'Meta': {'ordering': "['name']", 'object_name': 'AcademicTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'attestation.administrator': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'Administrator'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"})
        },
        'attestation.certifyingcommission': {
            'Meta': {'ordering': "['creation_date', 'expiration_date']", 'object_name': 'CertifyingCommission'},
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.CertifyingCommissionMember']", 'symmetrical': 'False'})
        },
        'attestation.certifyingcommissionmember': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'CertifyingCommissionMember'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Organization']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"}),
            'post_in_commission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.PostInCommission']"})
        },
        'attestation.degree': {
            'Meta': {'ordering': "['name']", 'object_name': 'Degree'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'attestation.education': {
            'Meta': {'ordering': "['id']", 'object_name': 'Education'},
            'diploma_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'qualification': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Request']"}),
            'speciality': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'attestation.expert': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'Expert'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Organization']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"})
        },
        'attestation.expertcommission': {
            'Meta': {'ordering': "['creation_date']", 'object_name': 'ExpertCommission'},
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Expert']", 'symmetrical': 'False'})
        },
        'attestation.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'abbreviate': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'settlement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Settlement']"})
        },
        'attestation.post': {
            'Meta': {'ordering': "['name']", 'object_name': 'Post'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'attestation.postincommission': {
            'Meta': {'ordering': "['name']", 'object_name': 'PostInCommission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_chairman': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vicechairman': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'attestation.qualification': {
            'Meta': {'ordering': "['name']", 'object_name': 'Qualification'},
            'for_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'request_form': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'attestation.request': {
            'Meta': {'ordering': "['id']", 'object_name': 'Request'},
            'academic_title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.AcademicTitle']", 'null': 'True', 'blank': 'True'}),
            'degree': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Degree']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'experience': ('django.db.models.fields.IntegerField', [], {}),
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['attestation.Expert']", 'null': 'True', 'blank': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Organization']", 'null': 'True', 'blank': 'True'}),
            'organization_experience': ('django.db.models.fields.IntegerField', [], {}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pedagogical_experience': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"}),
            'post_experience': ('django.db.models.fields.IntegerField', [], {}),
            'presence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Qualification']"}),
            'results': ('django.db.models.fields.TextField', [], {}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Territory']", 'null': 'True', 'blank': 'True'}),
            'trainings': ('django.db.models.fields.TextField', [], {}),
            'with_qualification': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'request_has_set'", 'null': 'True', 'to': "orm['attestation.Qualification']"})
        },
        'attestation.requestflow': {
            'Meta': {'ordering': "['date']", 'object_name': 'RequestFlow'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Request']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RequestStatus']"})
        },
        'attestation.requeststatus': {
            'Meta': {'ordering': "['name']", 'object_name': 'RequestStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_docs_received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_in_expertise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'attestation.settlement': {
            'Meta': {'ordering': "['name']", 'object_name': 'Settlement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.SettlementType']"})
        },
        'attestation.settlementtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'SettlementType'},
            'abbreviate': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'})
        },
        'attestation.territory': {
            'Meta': {'ordering': "['name']", 'object_name': 'Territory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'attestation.title': {
            'Meta': {'ordering': "['name']", 'object_name': 'Title'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['attestation']