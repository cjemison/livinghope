# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0023_auto_20150129_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialevent',
            name='display_on',
            field=models.DateField(null=True, verbose_name=b'Display on home page on this date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='description',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='home_page_image',
            field=livinghope.models.SmartImageField(help_text=b'This is the background image that                                    will be displayed on the homepage slider.<br>                                    This needs to be 1920x470 otherwise will look                                    strange.', null=True, upload_to=b'./event_images/', blank=True),
            preserve_default=True,
        ),
    ]
