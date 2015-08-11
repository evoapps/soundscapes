# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20150723_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='image',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='show',
            name='image_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
