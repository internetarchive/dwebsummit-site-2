# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

from django.contrib import admin
from django import forms

from adminsortable2.admin import SortableAdminMixin

from .models import (
    Person, Sponsor, TextField, Project, Page,
    NavbarLink, FooterLink, Video
)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    type = forms.ChoiceField(choices=[
        ('Participant', 'Participant'),
        ('Staff', 'Staff'),
        ('Featured', 'Featured'),
    ])

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'subtitle', 'type', 'is_attending_builders_day', 'is_featured_organizer')
    search_fields = ('first_name', 'last_name')
    list_filter = ('type', 'is_attending_builders_day', 'is_featured_organizer')
    form = PersonForm


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'type')


class ProjectForm(forms.ModelForm):
    short_description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':80}))
    search_fields = ('title',)
    list_filter = ('is_published',)
    class Meta:
        model = Project
        fields = '__all__'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('__unicode__', 'short_description', 'is_published')
    filter_horizontal = ('people',)



# Read the "page-templates" directory so those values can be used in the form
rootdir = os.path.join(
    os.path.dirname(__file__),
    '..',
    'dwebsummit_frontend',
    'templates',
    'dwebsummit',
    'page-templates'
)
for root, subdirs, files in os.walk(rootdir):
    # make sure text_page.html is first and default
    files.remove('text_page.html')
    files.insert(0, 'text_page.html')
    available_templates = [
        ( file, file.replace('_', ' ').replace('.html', '').title() )
        for file in files
    ]
    available_templates.sort()


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        exclude = ['prev_page']

    page_template = forms.ChoiceField(choices=available_templates)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['page_url'].help_text = 'Examples: "<code>proposals</code>",   "<code>about/internet-archive</code>". Leave blank for homepage'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('get_page_url', '__unicode__', 'is_published', 'page_template', )
    search_fields = ('page_url', 'title',)
    list_filter = ('is_published',)
    # TODO figure out how to get related videos in here
    filter_horizontal = ('people', 'related_pages',)

    def get_page_url(self, obj):
        return obj.page_url or '<home>'

@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(NavbarLink)
class NavbarLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'is_featured')
    pass


@admin.register(FooterLink)
class FooterLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    list_display = ('__unicode__', 'title', 'archive_identifier', 'is_featured')
    filter_horizontal = ('people', 'related_pages')
    readonly_fields = ('page_url', )


def bootstrap_data():
    """data_scaffold.yml contains some default db values
    This loads that initial data
    """
    # read yml file
    with open(os.path.join(os.path.dirname(__file__), 'data_scaffold.yml'), 'r') as stream:
        yaml_contents = yaml.load(stream)
        # Only creaet initial pages if no pages exist
        # (allows admins to delete pages in the future)
        if Page.objects.all().count() == 0:
            print 'Bootstrapping pages'
            for page_url in yaml_contents['pages']:
                obj, created = Page.objects.get_or_create(page_url=page_url)
                default_values = yaml_contents['pages'][page_url]
                if True or created:
                    obj.__dict__.update(**default_values)
                    obj.save()

try:
    bootstrap_data()
except Exception as detail:
    print detail
    pass



# Change admin site header title
admin.site.site_header = 'DWebSummit Admin'
