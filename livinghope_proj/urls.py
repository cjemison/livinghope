from django.conf.urls import patterns, include, url
from livinghope import urls as livinghope_urls
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('',
    url(r'^', include(livinghope_urls)),
)
