# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExpertInRequest'
        db.create_table('attestation_expertinrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Expert'])),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Request'])),
            ('first_grade', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('second_grade', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('attestation', ['ExpertInRequest'])

        # Removing M2M table for field experts on 'Request'
        db.delete_table('attestation_request_experts')


    def backwards(self, orm):
        # Deleting model 'ExpertInRequest'
        db.delete_table('attestation_expertinrequest')

        # Adding M2M table for field experts on 'Request'
        db.create_table('attestation_request_experts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm['attestation.request'], null=False)),
            ('expert', models.ForeignKey(orm['attestation.expert'], null=False))
        ))
        db.create_unique('attestation_request_experts', ['request_id', 'expert_id'])


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
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"})
        },
        'attestation.expertcommission': {
            'Meta': {'ordering': "['creation_date']", 'object_name': 'ExpertCommission'},
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Expert']", 'symmetrical': 'False'})
        },
        'attestation.expertinrequest': {
            'Meta': {'object_name': 'ExpertInRequest'},
            'expert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Expert']"}),
            'first_grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Request']"}),
            'second_grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Expert']", 'through': "orm['attestation.ExpertInRequest']", 'symmetrical': 'False'}),
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
            'secret_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'next_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RequestStatus']", 'null': 'True', 'blank': 'True'})
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