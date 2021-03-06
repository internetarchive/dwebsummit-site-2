# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 05:17
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwebsummit_admin', '0009_auto_20180627_0502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('short_description', models.CharField(blank=True, default='', max_length=255)),
                ('full_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='')),
                ('people', models.ManyToManyField(to='dwebsummit_admin.Person')),
            ],
            options={
                'verbose_name_plural': 'projects',
            },
        ),
    ]
