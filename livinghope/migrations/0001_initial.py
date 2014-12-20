# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Missionary'
        db.create_table(u'livinghope_missionary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image1_caption', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image2_caption', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image3_caption', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'livinghope', ['Missionary'])

        # Adding model 'Author'
        db.create_table(u'livinghope_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
        ))
        db.send_create_signal(u'livinghope', ['Author'])

        # Adding model 'Leader'
        db.create_table(u'livinghope_leader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('ministry', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('leadership_team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('small_group_leader', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
        ))
        db.send_create_signal(u'livinghope', ['Leader'])

        # Adding model 'BannerImage'
        db.create_table(u'livinghope_bannerimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('link_to', self.gf('django.db.models.fields.CharField')(default='#', max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'livinghope', ['BannerImage'])

        # Adding model 'Location'
        db.create_table(u'livinghope_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'livinghope', ['Location'])

        # Adding model 'SundaySchoolClass'
        db.create_table(u'livinghope_sundayschoolclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'livinghope', ['SundaySchoolClass'])

        # Adding model 'Service'
        db.create_table(u'livinghope_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('day', self.gf('django.db.models.fields.CharField')(default='SUN', max_length=4)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinghope.Location'])),
        ))
        db.send_create_signal(u'livinghope', ['Service'])

        # Adding model 'SmallGroup'
        db.create_table(u'livinghope_smallgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('day', self.gf('django.db.models.fields.CharField')(default='SUN', max_length=4)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinghope.Location'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'livinghope', ['SmallGroup'])

        # Adding M2M table for field leaders on 'SmallGroup'
        m2m_table_name = db.shorten_name(u'livinghope_smallgroup_leaders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('smallgroup', models.ForeignKey(orm[u'livinghope.smallgroup'], null=False)),
            ('leader', models.ForeignKey(orm[u'livinghope.leader'], null=False))
        ))
        db.create_unique(m2m_table_name, ['smallgroup_id', 'leader_id'])

        # Adding model 'PrayerMeeting'
        db.create_table(u'livinghope_prayermeeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('day', self.gf('django.db.models.fields.CharField')(default='SUN', max_length=4)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinghope.Location'])),
        ))
        db.send_create_signal(u'livinghope', ['PrayerMeeting'])

        # Adding model 'SermonSeries'
        db.create_table(u'livinghope_sermonseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('series_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('series_image_thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('passage_range', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('current_series', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'livinghope', ['SermonSeries'])

        # Adding model 'Sermon'
        db.create_table(u'livinghope_sermon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sermon_date', self.gf('django.db.models.fields.DateField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinghope.Author'])),
            ('sermon_series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['livinghope.SermonSeries'])),
            ('recording', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('passage', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('manuscript', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'livinghope', ['Sermon'])


    def backwards(self, orm):
        # Deleting model 'Missionary'
        db.delete_table(u'livinghope_missionary')

        # Deleting model 'Author'
        db.delete_table(u'livinghope_author')

        # Deleting model 'Leader'
        db.delete_table(u'livinghope_leader')

        # Deleting model 'BannerImage'
        db.delete_table(u'livinghope_bannerimage')

        # Deleting model 'Location'
        db.delete_table(u'livinghope_location')

        # Deleting model 'SundaySchoolClass'
        db.delete_table(u'livinghope_sundayschoolclass')

        # Deleting model 'Service'
        db.delete_table(u'livinghope_service')

        # Deleting model 'SmallGroup'
        db.delete_table(u'livinghope_smallgroup')

        # Removing M2M table for field leaders on 'SmallGroup'
        db.delete_table(db.shorten_name(u'livinghope_smallgroup_leaders'))

        # Deleting model 'PrayerMeeting'
        db.delete_table(u'livinghope_prayermeeting')

        # Deleting model 'SermonSeries'
        db.delete_table(u'livinghope_sermonseries')

        # Deleting model 'Sermon'
        db.delete_table(u'livinghope_sermon')


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
            'series_image_thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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