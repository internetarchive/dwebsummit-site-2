# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import yaml

from django.shortcuts import render
from django.views.generic import TemplateView


with open(os.path.join(os.path.dirname(__file__), 'contents.yml'), 'r') as stream:
    yaml_contents = yaml.load(stream)


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
        context['title'] = self.title.capitalize()

        # Data from the yaml file
        context['page'] = {
            'metadata': yaml_contents 
        }

        # TODO add access to models
        return context
