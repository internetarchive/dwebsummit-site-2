# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


# Change admin site header title
admin.site.site_header = 'DWebSummit Admin'
