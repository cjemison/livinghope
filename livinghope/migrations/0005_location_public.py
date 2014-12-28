# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0004_auto_20141227_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='public',
            field=models.BooleanField(default=False, help_text=b"Is this location's address OK to show publicly?"),
            preserve_default=True,
        ),
    ]
