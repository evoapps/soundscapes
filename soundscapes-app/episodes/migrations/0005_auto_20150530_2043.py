# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0004_auto_20150530_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='number',
        ),
        migrations.AddField(
            model_name='episode',
            name='released',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
