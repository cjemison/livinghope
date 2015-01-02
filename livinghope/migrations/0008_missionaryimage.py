# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0007_specialevent_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissionaryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'./missionary_images/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('caption', models.CharField(max_length=100, null=True, blank=True)),
                ('order', models.IntegerField(default=0, max_length=2)),
                ('missionary', models.ForeignKey(to='livinghope.Missionary')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
