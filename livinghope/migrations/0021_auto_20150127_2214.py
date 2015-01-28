# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0020_auto_20150126_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sermon',
            name='recording',
            field=models.FileField(null=True, upload_to=b'./sermon_recordings/', blank=True),
            preserve_default=True,
        ),
    ]
