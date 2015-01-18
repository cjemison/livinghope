# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0013_smallgroup_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmallGroupImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'./small_group_images/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('caption', models.CharField(max_length=100, null=True, blank=True)),
                ('order', models.IntegerField(default=0, max_length=2)),
                ('small_group', models.ForeignKey(to='livinghope.SmallGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='smallgroup',
            name='main_image',
            field=models.ImageField(null=True, upload_to=b'./small_group_images/', blank=True),
            preserve_default=True,
        ),
    ]
