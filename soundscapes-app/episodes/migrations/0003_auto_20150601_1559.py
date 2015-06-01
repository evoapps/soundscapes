# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0002_auto_20150601_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segment',
            name='episode',
        ),
        migrations.DeleteModel(
            name='Segment',
        ),
        migrations.AlterField(
            model_name='episode',
            name='mp3',
            field=models.FileField(max_length=200, null=True, upload_to=b'', blank=True),
        ),
    ]
