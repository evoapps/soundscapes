# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='moment',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='moment',
            name='episode',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='rss_mp3_url',
            new_name='mp3_url',
        ),
        migrations.RemoveField(
            model_name='segment',
            name='moments',
        ),
        migrations.DeleteModel(
            name='Moment',
        ),
        migrations.AddField(
            model_name='tag',
            name='segment',
            field=models.ForeignKey(related_query_name=b'tag', related_name='tags', to='manager.Segment'),
        ),
    ]
