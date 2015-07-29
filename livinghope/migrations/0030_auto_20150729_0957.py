# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0029_auto_20150726_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationposting',
            name='seeking',
            field=models.BooleanField(default=False, choices=[(True, b'Seeking'), (False, b'Donating')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='contact_email',
            field=models.EmailField(max_length=254, verbose_name=b'What email should responses be sent to?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='description',
            field=models.TextField(verbose_name=b'Briefly describe what you are donating or looking for', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='name',
            field=models.CharField(max_length=127, verbose_name=b'What are you donating or looking for?'),
            preserve_default=True,
        ),
    ]
