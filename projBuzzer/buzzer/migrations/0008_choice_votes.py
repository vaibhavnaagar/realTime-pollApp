# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buzzer', '0007_auto_20161101_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]