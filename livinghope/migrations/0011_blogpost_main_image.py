# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0010_auto_20150101_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='main_image',
            field=models.ImageField(null=True, upload_to=b'./blog_main_images/', blank=True),
            preserve_default=True,
        ),
    ]
