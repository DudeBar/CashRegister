# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Session', fields ['en_cours']
        db.create_index(u'Bar_session', ['en_cours'])


    def backwards(self, orm):
        # Removing index on 'Session', fields ['en_cours']
        db.delete_index(u'Bar_session', ['en_cours'])


    models = {
        u'Bar.barman': {
            'Meta': {'object_name': 'BarMan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'Bar.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['Bar.Category']", 'null': 'True', 'blank': 'True'})
        },
        u'Bar.commande': {
            'Meta': {'object_name': 'Commande'},
            'barman': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Bar.BarMan']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Bar.Session']"}),
            'total_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'Bar.commande_has_products': {
            'Meta': {'object_name': 'Commande_has_products'},
            'commande': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Bar.Commande']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Bar.Product']"})
        },
        u'Bar.config': {
            'Meta': {'object_name': 'Config'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variable': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'Bar.note': {
            'Meta': {'object_name': 'Note'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'Bar.product': {
            'Meta': {'object_name': 'Product'},
            'alert_stock': ('django.db.models.fields.IntegerField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Bar.Category']"}),
            'happy_hour': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'stock': ('django.db.models.fields.IntegerField', [], {}),
            'tva': ('django.db.models.fields.FloatField', [], {})
        },
        u'Bar.session': {
            'Meta': {'object_name': 'Session'},
            'en_cours': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'end_session': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_session': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'total_money': ('django.db.models.fields.FloatField', [], {'default': '0'})
        }
    }

    complete_apps = ['Bar']