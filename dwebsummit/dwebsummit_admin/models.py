# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify

from stdimage.models import StdImageField
from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField


class Person(models.Model):
    class Meta:
        verbose_name_plural = 'people'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, default='')
    bio = RichTextUploadingField(blank=True, default='')
    type = models.CharField(max_length=100, blank=True, default='Participant')

    image = StdImageField(variations={
        'thumbnail': { 'width': 500, 'height': 500, 'crop': True }
    })

    is_attending_builders_day = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def subtitle(self):
        parts = []
        if self.title:
            parts.append(self.title)
        if self.organization:
            parts.append(self.organization)
        return ', '.join(parts)

    def __unicode__(self):
        full_name = self.name
        if full_name:
            return full_name
        else:
            return 'Untitled person'



class Sponsor(models.Model):
    class Meta:
        verbose_name_plural = 'sponsors'

    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)

    REGULAR_SPONSOR = '0'
    LEAD_SPONSOR = '1'

    SPONSOR_TYPES = (
        (REGULAR_SPONSOR, 'Regular Sponsor'),
        (LEAD_SPONSOR, 'Lead Sponsor'),
    )

    type = models.CharField(
        max_length=2,
        choices=SPONSOR_TYPES,
        default=LEAD_SPONSOR,
    )

    image = StdImageField(variations={
        'thumbnail': { 'width': 500, 'height': 500, 'crop': False }
    })

    sponsorship_date = models.DateField()

    @property
    def slug(self):
        return slugify(self.title)

    def __unicode__(self):
        return self.title


class TextField(models.Model):
    class Meta:
        verbose_name_plural = 'text fields'

    name = models.CharField(max_length=100, blank=False, unique=True,
                            db_index=True, editable=False)
    value = RichTextUploadingField(blank=True, default='')

    def __unicode__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name_plural = 'projects'

    title = models.CharField(max_length=255, blank=True, default='')
    short_description = models.CharField(max_length=255, blank=True, default='')
    full_description = RichTextUploadingField(blank=True, default='')

    people = models.ManyToManyField(Person)

    is_published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title.strip() or 'Untitled project'



class Page(models.Model):
    """This model allows dynamic page creation in the admin"""
    class Meta:
        verbose_name_plural = 'pages'

    page_url = models.CharField(max_length=255, blank=True, unique=True, db_index=True)
    page_template = models.CharField(max_length=255, blank=True,
                                     default='text_page.html',
                                     help_text='Changes the html template.')

    title = models.CharField(max_length=255, blank=True, default='')

    banner_image = StdImageField(variations={
        'banner': { 'width': 1160, 'height': 420, 'crop': True},
        'banner_d': { 'width': 1160, 'height': 420, 'crop': True,
                      'effects': ['bw_dither']},
        'grid': { 'width': 370, 'height': 250, 'crop': True},
        'thumbnail': { 'width': 500, 'height': 500, 'crop': False }
    }, blank=True, null=True)

    body_text = RichTextUploadingField(blank=True, default='')

    next_page = models.ForeignKey('self', related_name='prev', blank=True, null=True)
    prev_page = models.ForeignKey('self', related_name='next', blank=True, null=True)

    people = models.ManyToManyField(Person, blank=True)

    related_pages = models.ManyToManyField('self', blank=True)

    is_published = models.BooleanField(default=True)

    @property
    def page_url_abs(self):
        if self.page_url == '':
            return '/'
        else:
            return '/' + self.page_url + '/'

    @property
    def person_list(self):
        """Returns a string representation of the people
        Uses .values for efficiency
        """
        values = self.people.all().values('first_name', 'last_name')
        names = [ v['first_name'] + ' ' + v['last_name'] for v in values ]
        return ', '.join(names)

    def __unicode__(self):
        title = self.title.strip() or 'Untitled page'
        return '/' + self.page_url + ' – ' + title + ''


class NavbarLink(models.Model):
    class Meta(object):
        ordering = ['sort_order']

    title = models.CharField(max_length=100, blank=False, default='')
    page = models.ForeignKey('Page', blank=True, null=True)
    external_url = models.URLField(max_length=255, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)
    is_featured = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title.strip() or 'Untitled link'


class FooterLink(models.Model):
    class Meta(object):
        ordering = ['sort_order']

    title = models.CharField(max_length=100, blank=False, default='')
    page = models.ForeignKey('Page', blank=True, null=True)
    external_url = models.URLField(max_length=255, blank=True, default='')
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.title.strip() or 'Untitled link'
