# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-29 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('firsttest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='group_points',
        ),
        migrations.RemoveField(
            model_name='player',
            name='points',
        ),
        migrations.AddField(
            model_name='group',
            name='group_ff_points',
            field=otree.db.models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='silo_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='ff_points',
            field=otree.db.models.IntegerField(default=0, null=True),
        ),
    ]