# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0022_auto_20150128_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to=b'./event_documents/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(to='livinghope.SpecialEvent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MinistryDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to=b'./ministry_documents/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ministry', models.ForeignKey(to='livinghope.Ministry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='specialevent',
            name='display_on_home_page',
            field=models.BooleanField(default=False, help_text=b'Should this be shown on the                                     home page slider when the event draws near?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='specialevent',
            name='home_page_image',
            field=livinghope.models.SmartImageField(null=True, upload_to=b'./event_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='specialevent',
            name='main_image',
            field=livinghope.models.SmartImageField(null=True, upload_to=b'./event_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='leadershiprole',
            name='special_name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionary',
            name='organization',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='main_image',
            field=livinghope.models.SmartImageField(help_text=b'This image will be displayed portrait-style                                              so landscape images will be cropped.', null=True, upload_to=b'./prayer_month_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermon',
            name='title',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermonseries',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
