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
                ('start_time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('end_time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('episode', models.ForeignKey(to='episodes.Episode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
