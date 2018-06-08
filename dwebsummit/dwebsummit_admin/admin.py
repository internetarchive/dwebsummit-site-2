# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Person, Sponsor

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'type')

    pass


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass


# Change admin site header title
admin.site.site_header = 'DWebSummit Admin'
