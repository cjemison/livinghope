# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0019_smallgroup_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('num_chapters', models.IntegerField(verbose_name=b'number of chapters')),
                ('order_index', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name=b'chapter')),
                ('num_verses', models.IntegerField(verbose_name=b'number of verses')),
                ('book', models.ForeignKey(to='livinghope.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('book', models.ForeignKey(to='livinghope.Book')),
                ('chapter', models.ForeignKey(to='livinghope.Chapter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sermon',
            name='verses',
            field=models.ManyToManyField(to='livinghope.Verse', blank=True),
            preserve_default=True,
        ),
    ]
