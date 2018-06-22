# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('dwebsummit_admin', '0006_auto_20180608_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('value', tinymce.models.HTMLField(blank=True, default='')),
            ],
            options={
                'verbose_name_plural': 'text fields',
            },
        ),
    ]
