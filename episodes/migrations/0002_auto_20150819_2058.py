# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='waveform',
            name='max',
            field=models.FloatField(default=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='waveform',
            name='min',
            field=models.FloatField(default=-10000),
            preserve_default=False,
        ),
    ]
