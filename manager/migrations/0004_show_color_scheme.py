# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20150811_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='color_scheme',
            field=models.TextField(default='["rgb(173,216,230)"]'),
            preserve_default=False,
        ),
    ]
