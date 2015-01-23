from django.conf.urls import patterns, include, url
from django.conf import settings
import views
from feeds import LatestSermonsFeed

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
    url(r'^childrens-ministry/$', views.childrens_ministry, name='childrens_ministry'),
    url(r'^missions/$', views.missions, name='missions'),
    url(r'^missionary/(?P<missionary_id>\d{1,8})/$', views.missionary_profile, name='missionary_profile'),
    url(r'^missions-prayer-calendar/$', views.prayer_calendar, name='missions_prayer_calendar'),
    url(r'^our-leaders/$', views.leaders, name='leaders'),
    url(r'^prayer/$', views.Prayer.as_view(), name='prayer'),
    url(r'^statement-of-faith/$', views.statement_of_faith, name='statement_of_faith'),
    url(r'^services/$', views.services, name='services'),
    url(r'^ministries/$', views.ministries, name='ministries'),
    url(r'^small-groups/$', views.small_groups, name='small_groups'),
    url(r'^contact/$', views.Contact.as_view(), name='contact'),

    #if you change these two, change in contact_leader.js
    url(r'^get_contact_leader_form/$', views.get_contact_leader_form, name='get_contact_leader_form'),
    url(r'^process_contact_leader_form/$', views.process_contact_leader_form, name='process_contact_leader_form'),
    
    url(r'^display-sermon-transcript/$', views.display_sermon_transcript, name='transcript_modal'),
    url(r'^report-broken-audio/$', views.report_broken_audio, name='broken_audio'),

    url(r'^blog/$', views.BlogHome.as_view(), name='blog'),
    url(r'^blog/entry/(?P<post_id>\d+)/$', views.BlogEntry.as_view(), name='blog_entry'),
    url(r'^blog/tag/(?P<tag_id>\d+)/$', views.BlogByTag.as_view(), name='blog_by_tag'),
    url(r'^blog/author/(?P<author_id>\d+)/$', views.BlogByAuthor.as_view(), name='blog_by_author'),
    url(r'^blog/year/(?P<year>\d{4})/$', views.BlogYear.as_view(), name='blog_by_year'),
    url(r'^blog/year/(?P<year>\d{4})/month/(?P<month>\d{1,2})/$', views.BlogMonth.as_view(), name='blog_by_month'),
    url(r'^blog/search/$', views.BlogSearch.as_view(), name='search_blog'),

    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^giving/$', views.giving, name='giving'),
    url(r'^events/$', views.events, name='events'),
    url(r'^our-denomination/$', views.denomination, name='denomination'),
    url(r'^display-event-details/$', views.display_event_details, name='event_details_modal'),

    url(r'^rss/latest-sermons/feed/$', LatestSermonsFeed()),
    # url(r'^paypal/create/$', views.paypal_create, name='paypal_create'),
    # url(r'^paypal/execute/$', views.paypal_execute, name='paypal_execute'),
    # url(r'^PayPal_IPN/$', views.paypal_payment_info_receiver),


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