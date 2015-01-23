# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0015_auto_20150121_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildrensMinistryClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_image', models.ImageField(upload_to=b'./childrens_ministry_images/')),
                ('youngest', models.CharField(help_text=b'What is the lower bound of the age range?', max_length=40)),
                ('oldest', models.CharField(help_text=b'What is the upper bound of the age range?', max_length=40)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChildrensMinistryTeacher',
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
            name='MissionsPrayerMonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('main_image', models.ImageField(null=True, upload_to=b'./prayer_month_images/', blank=True)),
                ('month', models.CharField(max_length=3, choices=[(b'JAN', b'January'), (b'FEB', b'February'), (b'MAR', b'March'), (b'APR', b'April'), (b'MAY', b'May'), (b'JUN', b'June'), (b'JUL', b'July'), (b'AUG', b'August'), (b'SEP', b'September'), (b'OCT', b'October'), (b'NOV', b'November'), (b'DEC', b'December')])),
                ('year', models.CharField(help_text=b'Enter full year not just 15', max_length=4)),
                ('prayer_requests', ckeditor.fields.RichTextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='missionsprayermonth',
            unique_together=set([('month', 'year')]),
        ),
        migrations.AddField(
            model_name='childrensministryclass',
            name='teachers',
            field=models.ManyToManyField(to='livinghope.ChildrensMinistryTeacher', null=True, blank=True),
            preserve_default=True,
        ),
    ]
