# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('episodes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DecimalField(max_digits=10, decimal_places=2)),
                ('value', models.FloatField()),
                ('episode', models.ForeignKey(related_name='moments', to='episodes.Episode')),
            ],
        ),
        migrations.AlterField(
            model_name='segment',
            name='episode',
            field=models.ForeignKey(related_name='segments', to='episodes.Episode'),
        ),
        migrations.AddField(
            model_name='segment',
            name='moments',
            field=models.ManyToManyField(related_name='moments', to='episodes.Moment'),
        ),
        migrations.AlterUniqueTogether(
            name='moment',
            unique_together=set([('episode', 'time')]),
        ),
    ]
