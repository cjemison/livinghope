# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0031_auto_20150803_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationposting',
            name='number_of_responses',
            field=models.IntegerField(default=0, max_length=3),
            preserve_default=True,
        ),
    ]
