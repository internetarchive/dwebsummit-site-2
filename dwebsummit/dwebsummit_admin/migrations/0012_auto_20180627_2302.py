# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('dwebsummit_admin', '0011_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='banner_image',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='page',
            name='next_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev', to='dwebsummit_admin.Page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='prev_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='dwebsummit_admin.Page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='thumbnail_image',
            field=stdimage.models.StdImageField(blank=True, null=True, upload_to=b''),
        ),
    ]
