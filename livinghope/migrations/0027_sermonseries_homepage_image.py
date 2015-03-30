# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0026_auto_20150315_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='sermonseries',
            name='homepage_image',
            field=models.ImageField(help_text=b'This image is the one that                                              will be displayed on the home page when                                              this series is the current series.                                               Ideally this should be 1920x470', null=True, upload_to=b'./sermon_series_home/', blank=True),
            preserve_default=True,
        ),
    ]
