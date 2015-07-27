# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0028_donationposting_donationpostingimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationposting',
            name='contact_name',
            field=models.CharField(default='test', max_length=127, verbose_name=b"What's your name?"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='contact_email',
            field=models.CharField(max_length=127, verbose_name=b'What email should responses be sent to?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='description',
            field=models.TextField(verbose_name=b'Briefly describe what you are donating', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='name',
            field=models.CharField(max_length=127, verbose_name=b'What are you donating?'),
            preserve_default=True,
        ),
    ]
