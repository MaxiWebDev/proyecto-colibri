# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Group.name'
        db.alter_column(u'parliamentarygroup_group', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Group.acronym'
        db.alter_column(u'parliamentarygroup_group', 'acronym', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

    def backwards(self, orm):

        # Changing field 'Group.name'
        db.alter_column(u'parliamentarygroup_group', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Group.acronym'
        db.alter_column(u'parliamentarygroup_group', 'acronym', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    models = {
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'congress_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'congress_web': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': "'50'"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscription_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'termination_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'twitter': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'parliamentarygroup.group': {
            'Meta': {'object_name': 'Group'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'congress_id': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '32'}),
            'congress_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'through': u"orm['parliamentarygroup.GroupMember']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['term.Term']"}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'parliamentarygroup.groupmember': {
            'Meta': {'object_name': 'GroupMember'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parliamentarygroup.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']"}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parliamentarygroup.Party']", 'null': 'True'})
        },
        u'parliamentarygroup.party': {
            'Meta': {'object_name': 'Party'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'validate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'web': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'term.term': {
            'Meta': {'object_name': 'Term'},
            'decimal': ('django.db.models.fields.IntegerField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 6, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roman': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 2, 6, 0, 0)'})
        }
    }

    complete_apps = ['parliamentarygroup']