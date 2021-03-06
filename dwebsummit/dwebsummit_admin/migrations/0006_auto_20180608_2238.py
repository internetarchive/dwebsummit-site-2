# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-08 22:38
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('dwebsummit_admin', '0005_auto_20180608_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_attending_builders_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='person',
            name='bio',
            field=tinymce.models.HTMLField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='person',
            name='organization',
            field=models.CharField(max_length=255),
        ),
    ]
