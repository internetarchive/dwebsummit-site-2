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
    type = models.CharField(max_length=100, blank=True, default='Participant')
    is_attending_builders_day = models.BooleanField(default=False)

    image = StdImageField(variations={
        'thumbnail': { 'width': 300, 'height': 300, 'crop': True },
        #'bw': { 'width': 200, 'height': 200, 'crop': True }
    })

    bio = RichTextUploadingField(blank=True, default='')

    is_featured_organizer = models.BooleanField(default=False,
                        help_text="Will be highlighted on people page")
    featured_organizer_text = models.TextField(blank=True, default='',
                        help_text="Short paragraph. Will be down next to iamge")

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
    INKIND_SPONSOR = '2'

    SPONSOR_TYPES = (
        (REGULAR_SPONSOR, 'Regular Sponsor'),
        (LEAD_SPONSOR, 'Lead Sponsor'),
        (INKIND_SPONSOR, 'In Kind Sponsor')
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
        'banner_d': { 'width': 1160, 'height': 420, 'crop': True, 'effects': ['dither']},
        'grid': { 'width': 370, 'height': 250, 'crop': True},
        'grid_d': { 'width': 406, 'height': 275, 'crop': True, 'effects': ['dither']}
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
    def has_grid_image(self):
        return bool(self.banner_image)

    @property
    def grid_image_url(self):
        return self.banner_image.grid.url

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

    def save(self, *args, **kwargs):
        # Make sure URLS are lowercase
        self.page_url = self.page_url.lower()
        return super(Page, self).save(*args, **kwargs)


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


class Video(models.Model):
    class Meta:
        verbose_name_plural = 'videos'

    title = models.CharField(max_length=255, blank=False, unique=True,
        help_text='The title of the video. Will also be used to generate the URL.')
    page_url = models.CharField(max_length=255, blank=False, unique=True,
                            db_index=True, editable=False,
                            help_text='This URL is generated from the title')
    archive_identifier = models.CharField(max_length=255, blank=False,
        help_text='Used to embed the video. eg. dweb-8_1_18_Front_End_Storiesfromthefield')

    thumbnail = StdImageField(variations={
        'grid': { 'width': 640, 'height': 360, 'crop': True},
        'grid_d': { 'width': 640, 'height': 360, 'crop': True, 'effects': ['dither']}
    }, blank=True, null=True)

    body_text = RichTextUploadingField(blank=True, default='')

    people = models.ManyToManyField(Person, blank=True)
    related_pages = models.ManyToManyField(Page, blank=True)

    is_featured = models.BooleanField(default=False, help_text='Will be shown at top of page')

    def __unicode__(self):
        return self.title.strip() or 'Untitled video'

    def save(self, *args, **kwargs):
        # Generate the page_url for the URL
        self.page_url = slugify(self.title)
        return super(Video, self).save(*args, **kwargs)

    @property
    def video_embed_url(self):
        return "https://archive.org/embed/" + self.archive_identifier

    @property
    def has_grid_image(self):
        return self.thumbnail is not None

    @property
    def grid_image_url(self):
        return self.thumbnail.grid.url

    @property
    def page_url_abs(self):
        return '/videos/' + self.page_url + '/'

    @property
    def person_list(self):
        """Returns a string representation of the people
        Uses .values for efficiency"""
        values = self.people.all().values('first_name', 'last_name')
        names = [ v['first_name'] + ' ' + v['last_name'] for v in values ]
        return ', '.join(names)

    next_prev_cache = None
    def next_prev(self):
        """For the video detail page, we link to a next and prev video, to keep the user engaged"""
        # inefficient, but it only runs on detail page
        if self.next_prev_cache is None:
            all_videos = Video.objects.all()
            match = False
            next_video = None
            prev_video = None
            index = 0
            for video in all_videos:
                if video.id == self.id:
                    next_video = all_videos[(index + 1) % len(all_videos)]
                    prev_video = all_videos[(index - 1) % len(all_videos)]
                    match = True
                    break
                index = index + 1

            if not match:
                next_video = all_videos[0]
                prev_video = all_videos[len(all_videos) - 1]

            self.next_prev_cache = (next_video, prev_video)
        return self.next_prev_cache

    @property
    def next_page(self):
        return self.next_prev()[0]

    @property
    def prev_page(self):
        return self.next_prev()[1]


