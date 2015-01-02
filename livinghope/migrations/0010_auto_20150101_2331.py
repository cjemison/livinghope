# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0009_auto_20150101_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadershipRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('special_name', models.CharField(max_length=100, null=True, blank=True)),
                ('primary_leader', models.BooleanField(default=False)),
                ('leader', models.ForeignKey(to='livinghope.Leader')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Ministries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leadershiprole',
            name='ministry',
            field=models.ForeignKey(to='livinghope.Ministry'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='leader',
            name='leadership_team',
        ),
        migrations.RemoveField(
            model_name='leader',
            name='ministry',
        ),
        migrations.RemoveField(
            model_name='leader',
            name='small_group_leader',
        ),
        migrations.AddField(
            model_name='leader',
            name='ministries',
            field=models.ManyToManyField(to='livinghope.Ministry', through='livinghope.LeadershipRole'),
            preserve_default=True,
        ),
    ]
