from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from livinghope.models import Sermon
import views
from mutagen.mp3 import MP3
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed

# For more details on the Podcast "Spec" see: https://www.apple.com/itunes/podcasts/specs.html

class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {u"version": self._version,
                u"xmlns:atom": u"http://www.w3.org/2005/Atom",
                u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['description'])
        handler.addQuickElement(u'itunes:explicit',
                                self.feed['iTunes_explicit'])
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['iTunes_name'])
        handler.addQuickElement(u'itunes:email', self.feed['iTunes_email'])
        handler.endElement(u"itunes:owner")
        handler.addQuickElement(u'itunes:image', self.feed['iTunes_image_url'])

    def add_item_elements(self, handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(
            handler, item)
        handler.addQuickElement(u'itunes:duration', item['duration'])
        handler.addQuickElement(u'itunes:explicit', item['explicit'])
        handler.addQuickElement(u'itunes:author', item['author'])


class LatestSermonsFeed(Feed):
    feed_type = iTunesPodcastsFeedGenerator
    title = "Living Hope Sermons"
    link = "/sitenews/"
    description = "The latest two sermons preached at Living Hope."
    subtitle = description
    summary = description
    iTunes_name = u'Free Law Project'
    iTunes_email = u'feeds@courtlistener.com'
    iTunes_image_url = u'https://www.courtlistener.com/static/png/producer.png'
    iTunes_explicit = u'no'

    def feed_extra_kwargs(self, obj):
        return {'iTunes_name': self.iTunes_name,
                'iTunes_email': self.iTunes_email,
                'iTunes_image_url': self.iTunes_image_url,
                'iTunes_explicit': self.iTunes_explicit}


    def item_extra_kwargs(self, item):
        audio = MP3(item.recording.path)
        duration = audio.info.length
        return {'author': item.author.full_name(),
                'duration': str(duration),
                'explicit': u'no'}

    def items(self):
        return Sermon.objects.all().exclude(recording='').order_by('-sermon_date')[:2]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.passage

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.recording.url

    def item_enclosure_url(self, item):
        return item.recording.url

    def item_enclosure_length(self,item):
        try:
            return item.recording.size
        except:
            return 5000

    item_enclosure_mime_type = 'audio/mpeg'
    # def item_enclosure_mime_type(self, item):
