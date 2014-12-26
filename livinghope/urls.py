from django.conf.urls import patterns, include, url
from django.conf import settings
import views

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home),
    url(r'^sermon-series/$', views.sermon_series, name='sermon_series'),
    url(r'^sermon-series/(?P<series_id>\d{1,8})/$', views.sermon_series, name='sermon_series'),
    url(r'^missionaries/$', views.missionaries, name='missionaries'),
    url(r'^missionary/(?P<missionary_id>\d{1,8})/$', views.missionary_profile, name='missionary_profile'),
    url(r'^our-leaders/$', views.leaders, name='leaders'),
    url(r'^prayer/$', views.Prayer.as_view(), name='prayer'),
    url(r'^statement-of-faith/$', views.statement_of_faith, name='statement_of_faith'),
    url(r'^services/$', views.services, name='services'),
    url(r'^ministries/$', views.ministries, name='ministries'),
    url(r'^contact/$', views.Contact.as_view(), name='contact'),
    url(r'^display-sermon-transcript/$', views.display_sermon_transcript, name='transcript_modal'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^blog/entry/(?P<blog_id>\d+)/$', views.blog_entry, name='blog_entry'),
    url(r'^blog/year/(?P<year>\d{4})/$', views.blog_by_year, name='blog_by_year'),
    url(r'^blog/year/(?P<year>\d{4})/month/(?P<month>\d{1,2})/$', views.blog_by_month, name='blog_by_month'),
    (r'^ckeditor/', include('ckeditor.urls')),
    ##onetime utilities
    url(r'^load-sermons/$', views.load_sermons),

)

if settings.DEBUG:
    import debug_toolbar
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))