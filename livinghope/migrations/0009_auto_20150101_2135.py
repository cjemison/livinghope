# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0008_missionaryimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missionary',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='missionary',
            name='image1_caption',
        ),
        migrations.RemoveField(
            model_name='missionary',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='missionary',
            name='image2_caption',
        ),
        migrations.RemoveField(
            model_name='missionary',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='missionary',
            name='image3_caption',
        ),
    ]
