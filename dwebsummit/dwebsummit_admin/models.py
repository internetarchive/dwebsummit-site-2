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

    def __unicode__(self):
        return self.title.strip() or 'Untitled project'
