# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0011_blogpost_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sermonseries',
            name='description',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='main_image',
            field=models.ImageField(help_text=b'For best results, the width of the image                                                 should be larger than the height. Ideally                                                 5:3 aspect ratio', null=True, upload_to=b'./blog_main_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='leader',
            name='bio',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionary',
            name='bio',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
