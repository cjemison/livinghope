# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0021_auto_20150127_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='missionsprayermonth',
            name='missionary',
        ),
        migrations.AlterField(
            model_name='bannerimage',
            name='link_to',
            field=models.CharField(default=b'#', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='street_address',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionary',
            name='website',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionaryimage',
            name='caption',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='missionsprayermonth',
            name='highlight',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sermon',
            name='passage',
            field=models.CharField(help_text=b'\n                        Do not abbreviate book names. Separate verses by commas\n                        and always include chapter number if applicable.<br>\n                        If the passage spans whole chapters, it\'s acceptable to \n                        separate chapter numbers with a "-" if book name is given.<br>\n                        Good, very clear: Philippians 1:1-3, 1:6-8, 1 John 1 <br>\n                        Bad, ambiguous: Phi. 1:1-3, 6-8. Is this Philippians or Philemon? \n                        6-8 would be interpreted as chapters 6-8 not verses 1:6-8\n                        ', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smallgroupimage',
            name='caption',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
