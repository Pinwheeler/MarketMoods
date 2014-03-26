__author__ = 'anthonydreessen'

from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'linegraph.views.index'),
)