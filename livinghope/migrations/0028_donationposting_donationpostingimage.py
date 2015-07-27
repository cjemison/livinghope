# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0027_sermonseries_homepage_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationPosting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('contact_email', models.CharField(max_length=127)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DonationPostingImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', livinghope.models.SmartImageField(upload_to=b'./donation_images/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=127)),
                ('donation_posting', models.ForeignKey(to='livinghope.DonationPosting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
