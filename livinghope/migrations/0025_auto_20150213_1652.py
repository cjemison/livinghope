# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0024_auto_20150130_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='missionsprayermonth',
            name='main_image_caption',
            field=models.CharField(help_text=b'Brief description of the image', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='childrensministryclass',
            name='order',
            field=models.IntegerField(default=0, help_text=b"This determines the ordering of classes                                on the Children's ministry page.", max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='highlight',
            field=models.CharField(default=b'', help_text=b'What is being highlighted this month?', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermon',
            name='sermon_date',
            field=models.DateField(help_text=b'When was the sermon preached?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermonseries',
            name='current_series',
            field=models.BooleanField(default=False, help_text=b'Is this the current series?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='display_on_home_page',
            field=models.BooleanField(default=False, help_text=b'Should this be shown on the                                     home page slider when the event approaches?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='main_image',
            field=livinghope.models.SmartImageField(help_text=b'This is the image that will be                                    displayed on the event page. NOT displayed on                                    the home page.', null=True, upload_to=b'./event_images/', blank=True),
            preserve_default=True,
        ),
    ]
