# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0018_auto_20150123_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='smallgroup',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
