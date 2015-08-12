# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_waveform'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waveform',
            name='id',
        ),
        migrations.AlterField(
            model_name='waveform',
            name='episode',
            field=models.OneToOneField(primary_key=True, serialize=False, to='manager.Episode'),
        ),
    ]
