# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0005_location_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('day', models.CharField(default=b'SUN', max_length=4, choices=[(b'MON', b'Monday'), (b'TUES', b'Tuesday'), (b'WED', b'Wednesday'), (b'THU', b'Thursday'), (b'FRI', b'Friday'), (b'SAT', b'Saturday'), (b'SUN', b'Sunday')])),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('description', models.TextField(null=True, blank=True)),
                ('location', models.ForeignKey(to='livinghope.Location')),
                ('organizer', models.ManyToManyField(to='livinghope.Leader')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
