# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_auto_20170927_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='cgst_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='igst_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='sgst_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
