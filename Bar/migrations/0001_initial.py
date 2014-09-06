# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BarMan'
        db.create_table(u'Bar_barman', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'Bar', ['BarMan'])

        # Adding model 'Category'
        db.create_table(u'Bar_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['Bar.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'Bar', ['Category'])

        # Adding model 'Session'
        db.create_table(u'Bar_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_session', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_session', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('total_money', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('en_cours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Bar', ['Session'])

        # Adding model 'Product'
        db.create_table(u'Bar_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Bar.Category'])),
            ('stock', self.gf('django.db.models.fields.IntegerField')()),
            ('alert_stock', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('happy_hour', self.gf('django.db.models.fields.FloatField')()),
            ('tva', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'Bar', ['Product'])

        # Adding model 'Commande'
        db.create_table(u'Bar_commande', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('barman', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Bar.BarMan'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Bar.Session'])),
            ('total_price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'Bar', ['Commande'])

        # Adding model 'Commande_has_products'
        db.create_table(u'Bar_commande_has_products', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('commande', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Bar.Commande'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Bar.Product'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'Bar', ['Commande_has_products'])

        # Adding model 'Config'
        db.create_table(u'Bar_config', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variable', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'Bar', ['Config'])


    def backwards(self, orm):
        # Deleting model 'BarMan'
        db.delete_table(u'Bar_barman')

        # Deleting model 'Category'
        db.delete_table(u'Bar_category')

        # Deleting model 'Session'
        db.delete_table(u'Bar_session')

        # Deleting model 'Product'
        db.delete_table(u'Bar_product')

        # Deleting model 'Commande'
        db.delete_table(u'Bar_commande')

        # Deleting model 'Commande_has_products'
        db.delete_table(u'Bar_commande_has_products')

        # Deleting model 'Config'
        db.delete_table(u'Bar_config')


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
            'en_cours': ('django.db.models.fields.IntegerField', [], {}),
            'end_session': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_session': ('django.db.models.fields.DateTimeField', [], {}),
            'total_money': ('django.db.models.fields.FloatField', [], {'default': '0'})
        }
    }

    complete_apps = ['Bar']