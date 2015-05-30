# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0002_episode_mp3'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='episode',
            name='name',
            field=models.CharField(max_length=80, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='number',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='show',
            field=models.ForeignKey(blank=True, to='episodes.Show', null=True),
            preserve_default=True,
        ),
    ]
