import os
from django.conf import settings
from django.conf.urls import url

from .views import WithDataTemplateView, PageDetailView, VideoDetailView


urlpatterns = [
    url(r'^videos/(?P<slug>[\w\-_\/]+)/$', VideoDetailView.as_view(), name='video_detail'),
    url(r'^(?P<slug>[\w\-_\/]+)/$', PageDetailView.as_view(), name='page_detail'),
    url(r'^$', PageDetailView.as_view(), name='home_detail'),
]
