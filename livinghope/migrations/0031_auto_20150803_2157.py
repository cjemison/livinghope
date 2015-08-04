# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0030_auto_20150729_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='donationposting',
            name='seeking',
            field=models.BooleanField(default=False, verbose_name=b'Are you donating or seeking?', choices=[(True, b'Seeking'), (False, b'Donating')]),
            preserve_default=True,
        ),
    ]
