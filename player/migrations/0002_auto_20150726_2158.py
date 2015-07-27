# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segmentbubble',
            name='episode',
        ),
        migrations.AlterField(
            model_name='horizonline',
            name='episode',
            field=models.OneToOneField(related_name='horizon_line', to='manager.Episode'),
        ),
        migrations.DeleteModel(
            name='SegmentBubble',
        ),
    ]
