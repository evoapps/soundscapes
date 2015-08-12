# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_show_color_scheme'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waveform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interval', models.IntegerField()),
                ('values', models.TextField()),
                ('episode', models.OneToOneField(related_name='waveform', to='manager.Episode')),
            ],
        ),
    ]
