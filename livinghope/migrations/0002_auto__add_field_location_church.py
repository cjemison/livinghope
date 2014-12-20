# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.church'
        db.add_column(u'livinghope_location', 'church',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Location.church'
        db.delete_column(u'livinghope_location', 'church')


    models = {
        u'livinghope.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'livinghope.bannerimage': {
            'Meta': {'object_name': 'BannerImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link_to': ('django.db.models.fields.CharField', [], {'default': "'#'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        u'livinghope.leader': {
            'Meta': {'object_name': 'Leader'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'leadership_team': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ministry': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'small_group_leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'livinghope.location': {
            'Meta': {'object_name': 'Location'},
            'church': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'livinghope.missionary': {
            'Meta': {'object_name': 'Missionary'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image1_caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image2_caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image3_caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'livinghope.prayermeeting': {
            'Meta': {'object_name': 'PrayerMeeting'},
            'day': ('django.db.models.fields.CharField', [], {'default': "'SUN'", 'max_length': '4'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinghope.Location']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'livinghope.sermon': {
            'Meta': {'object_name': 'Sermon'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinghope.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manuscript': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'passage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'recording': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'sermon_date': ('django.db.models.fields.DateField', [], {}),
            'sermon_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinghope.SermonSeries']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'livinghope.sermonseries': {
            'Meta': {'object_name': 'SermonSeries'},
            'current_series': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'passage_range': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'series_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'series_image_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'livinghope.service': {
            'Meta': {'object_name': 'Service'},
            'day': ('django.db.models.fields.CharField', [], {'default': "'SUN'", 'max_length': '4'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinghope.Location']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'livinghope.smallgroup': {
            'Meta': {'object_name': 'SmallGroup'},
            'day': ('django.db.models.fields.CharField', [], {'default': "'SUN'", 'max_length': '4'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['livinghope.Leader']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['livinghope.Location']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'livinghope.sundayschoolclass': {
            'Meta': {'object_name': 'SundaySchoolClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['livinghope']