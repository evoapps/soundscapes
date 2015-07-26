# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20150723_0028'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorizonLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heights', models.TextField()),
                ('interval', models.IntegerField()),
                ('episode', models.OneToOneField(to='manager.Episode')),
            ],
        ),
        migrations.CreateModel(
            name='SegmentBubble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.IntegerField()),
                ('episode', models.ForeignKey(to='manager.Episode')),
            ],
        ),
    ]
