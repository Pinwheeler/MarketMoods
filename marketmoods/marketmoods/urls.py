__author__ = 'anthonydreessen'

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:

                       # url(r'^blog/', include('blog.urls')),
                       url(r'^graphs/', include('graphs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'marketmoods.views.home', name='home'),
)
