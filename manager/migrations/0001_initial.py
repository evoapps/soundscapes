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
                ('rss_mp3_url', models.URLField(unique=True)),
                ('mp3', models.FileField(max_length=200, upload_to=b'', blank=True)),
                ('duration', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('value', models.FloatField()),
                ('episode', models.ForeignKey(related_name='moments', to='manager.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('end_time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('episode', models.ForeignKey(related_name='segments', to='manager.Episode')),
                ('moments', models.ManyToManyField(related_name='moments', to='manager.Moment')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('rss_url', models.URLField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(to='manager.Show'),
        ),
        migrations.AlterUniqueTogether(
            name='moment',
            unique_together=set([('episode', 'time')]),
        ),
    ]
