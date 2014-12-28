# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0003_blogpost_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermon',
            name='manuscript',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
