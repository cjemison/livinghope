# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0016_auto_20150122_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='childrensministryclass',
            name='order',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='childrensministryclass',
            name='main_image',
            field=models.ImageField(null=True, upload_to=b'./childrens_ministry_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ministry',
            name='description',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='month',
            field=models.IntegerField(max_length=2, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='year',
            field=models.IntegerField(help_text=b'Enter full year not just 15', max_length=4),
            preserve_default=True,
        ),
    ]
