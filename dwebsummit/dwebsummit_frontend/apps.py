# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.staticfiles.apps import StaticFilesConfig


class DwebsummitFrontendConfig(AppConfig):
    name = 'dwebsummit_frontend'


class CustomStaticFilesConfig(StaticFilesConfig):
    """This is overridden so that scss is copied into the public directory"""
    ignore_patterns = ['CVS', '.*', '*~', '*.scss']
