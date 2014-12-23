# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BannerImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25, null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'./banner_images/', blank=True)),
                ('order', models.IntegerField(max_length=2)),
                ('link_to', models.CharField(default=b'#', max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Leader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'./leader_images/', blank=True)),
                ('ministry', models.CharField(max_length=100)),
                ('leadership_team', models.BooleanField(default=False)),
                ('small_group_leader', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField(default=0, max_length=2)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('street_address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=10)),
                ('church', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Missionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('profile_picture', models.ImageField(null=True, upload_to=b'./missionary_images/', blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('organization', models.CharField(max_length=100, null=True, blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('image1', models.ImageField(null=True, upload_to=b'./missionary_images/', blank=True)),
                ('image1_caption', models.CharField(max_length=50, null=True, blank=True)),
                ('image2', models.ImageField(null=True, upload_to=b'./missionary_images/', blank=True)),
                ('image2_caption', models.CharField(max_length=50, null=True, blank=True)),
                ('image3', models.ImageField(null=True, upload_to=b'./missionary_images/', blank=True)),
                ('image3_caption', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Missionaries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PrayerMeeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('day', models.CharField(default=b'SUN', max_length=4, choices=[(b'MON', b'Monday'), (b'TUES', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')])),
                ('location', models.ForeignKey(to='livinghope.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sermon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sermon_date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('recording', models.FileField(upload_to=b'./sermon_recordings/')),
                ('passage', models.CharField(max_length=50, null=True, blank=True)),
                ('manuscript', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(to='livinghope.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SermonSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('series_image', models.ImageField(null=True, upload_to=b'./sermon_series/', blank=True)),
                ('series_image_thumbnail', models.ImageField(null=True, upload_to=b'./sermon_series_thumb/')),
                ('passage_range', models.CharField(max_length=50)),
                ('current_series', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Sermon Series',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('day', models.CharField(default=b'SUN', max_length=4, choices=[(b'MON', b'Monday'), (b'TUES', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')])),
                ('location', models.ForeignKey(to='livinghope.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmallGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('day', models.CharField(default=b'SUN', max_length=4, choices=[(b'MON', b'Monday'), (b'TUES', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')])),
                ('region', models.CharField(max_length=30)),
                ('leaders', models.ManyToManyField(to='livinghope.Leader', null=True, blank=True)),
                ('location', models.ForeignKey(to='livinghope.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SundaySchoolClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sermon',
            name='sermon_series',
            field=models.ForeignKey(to='livinghope.SermonSeries'),
            preserve_default=True,
        ),
    ]
