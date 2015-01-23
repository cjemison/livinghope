# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0017_auto_20150122_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='missionsprayermonth',
            name='highlight',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='missionsprayermonth',
            name='missionary',
            field=models.ForeignKey(blank=True, to='livinghope.Missionary', help_text=b'Put this in if the highlight is also a missionary we support', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='main_image',
            field=livinghope.models.SmartImageField(help_text=b'For best results, the width of the image                                                 should be larger than the height. Ideally                                                 5:3 aspect ratio', null=True, upload_to=b'./blog_main_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='childrensministryclass',
            name='main_image',
            field=livinghope.models.SmartImageField(null=True, upload_to=b'./childrens_ministry_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='main_image',
            field=livinghope.models.SmartImageField(null=True, upload_to=b'./prayer_month_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smallgroup',
            name='main_image',
            field=livinghope.models.SmartImageField(null=True, upload_to=b'./small_group_images/', blank=True),
            preserve_default=True,
        ),
    ]
