# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('episode', models.ForeignKey(to='episodes.Episode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='episode',
            name='mp3',
            field=models.FileField(max_length=200, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='episode',
            name='released',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(to='episodes.Show'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
