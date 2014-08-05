# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Achievement'
        db.create_table('attestation_achievement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('attestation', ['Achievement'])

        # Deleting field 'Request.degree'
        db.delete_column('attestation_request', 'degree_id')

        # Adding M2M table for field degrees on 'Request'
        db.create_table('attestation_request_degrees', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm['attestation.request'], null=False)),
            ('degree', models.ForeignKey(orm['attestation.degree'], null=False))
        ))
        db.create_unique('attestation_request_degrees', ['request_id', 'degree_id'])

        # Adding M2M table for field achievements on 'Request'
        db.create_table('attestation_request_achievements', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('request', models.ForeignKey(orm['attestation.request'], null=False)),
            ('achievement', models.ForeignKey(orm['attestation.achievement'], null=False))
        ))
        db.create_unique('attestation_request_achievements', ['request_id', 'achievement_id'])


    def backwards(self, orm):
        # Deleting model 'Achievement'
        db.delete_table('attestation_achievement')

        # Adding field 'Request.degree'
        db.add_column('attestation_request', 'degree',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['attestation.Degree'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field degrees on 'Request'
        db.delete_table('attestation_request_degrees')

        # Removing M2M table for field achievements on 'Request'
        db.delete_table('attestation_request_achievements')


    models = {
        'attestation.academictitle': {
            'Meta': {'ordering': "['name']", 'object_name': 'AcademicTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'attestation.achievement': {
            'Meta': {'ordering': "['name']", 'object_name': 'Achievement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'attestation.area': {
            'Meta': {'ordering': "['name']", 'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'attestation.certifyingcommission': {
            'Meta': {'ordering': "['creation_date', 'expiration_date']", 'object_name': 'CertifyingCommission'},
            'chairman': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'chairman'", 'null': 'True', 'to': "orm['attestation.CertifyingCommissionMember']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.CertifyingCommissionMember']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'secretary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secretary'", 'null': 'True', 'to': "orm['attestation.CertifyingCommissionMember']"}),
            'vice_chairman': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'vice'", 'null': 'True', 'to': "orm['attestation.CertifyingCommissionMember']"})
        },
        'attestation.certifyingcommissionmember': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'CertifyingCommissionMember'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'attestation.config': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Config'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'first_stage_max_grade': ('django.db.models.fields.IntegerField', [], {}),
            'first_stage_min_grade': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_stage_max_grade': ('django.db.models.fields.IntegerField', [], {}),
            'second_stage_min_grade': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateField', [], {})
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
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Area']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'organization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Territory']", 'null': 'True', 'blank': 'True'})
        },
        'attestation.expertinrequest': {
            'Meta': {'ordering': "['expert__last_name']", 'object_name': 'ExpertInRequest'},
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'attestation.qualification': {
            'Meta': {'ordering': "['name']", 'object_name': 'Qualification'},
            'for_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'request_form': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'result_form': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'attestation.request': {
            'Meta': {'ordering': "['id']", 'object_name': 'Request'},
            'academic_title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.AcademicTitle']", 'null': 'True', 'blank': 'True'}),
            'achievements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Achievement']", 'symmetrical': 'False'}),
            'agree': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'decision': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Degree']", 'symmetrical': 'False'}),
            'disagree': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'experience': ('django.db.models.fields.IntegerField', [], {}),
            'experts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attestation.Expert']", 'through': "orm['attestation.ExpertInRequest']", 'symmetrical': 'False'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number_of_members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Organization']", 'null': 'True', 'blank': 'True'}),
            'organization_experience': ('django.db.models.fields.IntegerField', [], {}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pedagogical_experience': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Post']"}),
            'post_date': ('django.db.models.fields.DateField', [], {}),
            'post_experience': ('django.db.models.fields.IntegerField', [], {}),
            'presence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.Qualification']"}),
            'recomendations': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'next_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['attestation.RequestStatus']", 'null': 'True', 'blank': 'True'}),
            'simple_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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