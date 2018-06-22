# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

from django.contrib import admin

from .models import Person, Sponsor, TextField

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'type')
    pass


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'type')
    pass


@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    pass


# Data_scaffold contains text fields with some defaults
def ensure_text_fields_exist():
    # read yml file
    with open(os.path.join(os.path.dirname(__file__), 'data_scaffold.yml'), 'r') as stream:
        yaml_contents = yaml.load(stream)
        for name in yaml_contents['text_fields']:
            obj, created = TextField.objects.get_or_create(name=name)
            if created:
                obj.value = yaml_contents['text_fields'][name]
                obj.save()


ensure_text_fields_exist()

# Change admin site header title
admin.site.site_header = 'DWebSummit Admin'
