# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0014_auto_20150118_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sermonseries',
            name='series_image_thumbnail',
        ),
        migrations.AlterField(
            model_name='sermonseries',
            name='series_image',
            field=models.ImageField(default=0, help_text=b'Image should be ideally                                                1500x1125 or 720x540', upload_to=b'./sermon_series/'),
            preserve_default=False,
        ),
    ]
