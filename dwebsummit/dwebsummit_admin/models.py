# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from stdimage.models import StdImageField
from tinymce.models import HTMLField


class Person(models.Model):
    class Meta:
        verbose_name_plural = 'people'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255, blank=True, default='')
    bio = HTMLField()
    type = models.CharField(max_length=100, blank=True, default='Participant')

    image = StdImageField(variations={
        'thumbnail': {'width': 500, 'height': 500, 'crop': True}
    })

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

    @property
    def image_url(self):
        if self.image and self.image.url:
            return self.image.url
        else:
            return '/static/img/brewster-kahle.jpg' # TODO default image

    def __unicode__(self):
        full_name = self.name
        if full_name:
            return full_name
        else:
            return 'Untitled person'
