# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView

from dwebsummit_admin.models import (
    Person, Sponsor, TextField, Project, Page, FooterLink, NavbarLink
)


with open(os.path.join(os.path.dirname(__file__), 'contents.yml'), 'r') as stream:
    yaml_contents = yaml.load(stream)


def build_context_data(context):
    # context['title'] = self.title.capitalize()

    # Data from the yaml file
    context['page'] = {
        'metadata': yaml_contents
    }

    context['people'] = Person.objects.all().order_by('first_name')
    context['lead_sponsors'] = Sponsor.objects.filter(type=Sponsor.LEAD_SPONSOR)
    context['sponsors'] = Sponsor.objects.filter(type=Sponsor.REGULAR_SPONSOR)
    context['text_fields'] = TextField.objects.all()
    context['projects'] = Project.objects.filter(is_published=True).order_by('title')
    context['builders_day_projects'] = Project.objects.filter(is_published=True,
                                            people__is_attending_builders_day=True).distinct().order_by('title')
    context['footer_links'] = FooterLink.objects.all().prefetch_related('page').order_by('sort_order')
    context['navbar_links'] = NavbarLink.objects.all().prefetch_related('page').order_by('sort_order')


class WithDataTemplateView(TemplateView):
    """
    This helper class provides handles to basic information from the CMS
    that can be used in the templates.

    This makes the frontend work more like a static site builder, where the
    templates define the routes, and they have access to the data directly.

    Note since django's ORM lazily excutes queries, we can include a lot of
    handles, but it does not impact performance.
    """

    # Title is the page name (renders it into css)
    title = ''

    def get_context_data(self, **kwargs):
        context = super(WithDataTemplateView, self).get_context_data(**kwargs)
        build_context_data(context)
        return context


class PageDetailView(DetailView):
    model = Page
    slug_url_kwarg = 'page_url'

    def get_object(self):
        slug = self.kwargs.get('slug', '')
        slug = slug.lower()
        return get_object_or_404(Page, page_url=slug, is_published=True)

    def get_template_names(self, **kwargs):
        return [ 'dwebsummit/page-templates/' + self.object.page_template ]
        return super(PageDetailView, self).get_template_names(**kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['title'] = self.object.title.capitalize()

        # Add additional context
        build_context_data(context)
        return context
