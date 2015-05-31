# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0006_auto_20150531_0426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='episode',
            old_name='soundcloud_track_id',
            new_name='soundcloud_id',
        ),
    ]
