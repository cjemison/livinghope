# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import livinghope.models


class Migration(migrations.Migration):

    dependencies = [
        ('livinghope', '0025_auto_20150213_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='SermonDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to=b'./sermon_documents/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('sermon', models.ForeignKey(to='livinghope.Sermon')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='smallgroup',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Only small groups marked as active will be                                 displayed on the small groups page'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smallgroup',
            name='leaders',
            field=models.ManyToManyField(help_text=b'This is currently optional and will                                      not actually display publicly', to='livinghope.Leader', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smallgroup',
            name='main_image',
            field=livinghope.models.SmartImageField(help_text=b'This image will be displayed at the top                                    of your small group section on the small groups page', null=True, upload_to=b'./small_group_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialevent',
            name='organizer',
            field=models.ManyToManyField(help_text=b'This is who the main point of contact                                       should be for this event.', to='livinghope.Leader'),
            preserve_default=True,
        ),
    ]
