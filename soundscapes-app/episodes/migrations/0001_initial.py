# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import episodes.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('released', models.DateTimeField()),
                ('title', models.CharField(max_length=80)),
                ('rss', models.URLField(unique=True)),
                ('mp3', models.FileField(storage=episodes.models.EpisodeFileStorage(), max_length=200, null=True, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('rss', models.URLField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(to='episodes.Show'),
            preserve_default=True,
        ),
    ]
