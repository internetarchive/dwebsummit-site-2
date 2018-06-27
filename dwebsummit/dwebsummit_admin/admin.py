# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

from django.contrib import admin
from django import forms

from .models import Person, Sponsor, TextField, Project

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'type')


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'type')


class ProjectForm(forms.ModelForm):
    short_description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':80}))
    class Meta:
        model = Project
        fields = '__all__'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('__unicode__', 'short_description', )
    filter_horizontal = ('people',)


@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)


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

try:
    ensure_text_fields_exist()
except:
    pass

# Change admin site header title
admin.site.site_header = 'DWebSummit Admin'
