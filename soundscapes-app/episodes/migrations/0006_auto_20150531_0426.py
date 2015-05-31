# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0005_auto_20150530_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='soundcloud_track_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='show',
            name='soundcloud_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='show',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
