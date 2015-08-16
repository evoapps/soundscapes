# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('rss_entry', models.TextField()),
                ('released', models.DateTimeField()),
                ('title', models.CharField(max_length=80)),
                ('duration', models.FloatField(null=True)),
                ('mp3_url', models.URLField(unique=True)),
                ('mp3', models.FileField(max_length=200, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('end_time', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('rss_url', models.URLField(unique=True)),
                ('image_url', models.URLField()),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('color_scheme', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('segment', models.ForeignKey(related_query_name=b'tag', related_name='tags', to='episodes.Segment')),
            ],
        ),
        migrations.CreateModel(
            name='Waveform',
            fields=[
                ('episode', models.OneToOneField(primary_key=True, serialize=False, to='episodes.Episode')),
                ('interval', models.IntegerField()),
                ('values', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='segment',
            name='episode',
            field=models.ForeignKey(related_name='segments', to='episodes.Episode'),
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(to='episodes.Show'),
        ),
    ]
