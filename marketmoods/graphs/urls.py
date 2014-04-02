__author__ = 'anthonydreessen'

from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^line', 'graphs.views.linegraph'),
                       url(r'^toggle', 'graphs.views.toggle'),
                       url(r'^current-data', 'graphs.views.current_data'),
                       url(r'^search', 'graphs.views.search'),
)