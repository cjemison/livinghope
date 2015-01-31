from django.contrib.syndication.views import Feed
from django.templatetags.static import static
from django.core.urlresolvers import reverse
from livinghope.models import Sermon
import views
from mutagen.mp3 import MP3
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from datetime import datetime, time
from easy_thumbnails.files import get_thumbnailer
from django.conf import settings
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
        handler.addQuickElement(u'itunes:image', attrs={"href":self.feed['iTunes_image_url']})

    def add_item_elements(self, handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(
            handler, item)
        handler.addQuickElement(u'itunes:duration', item['duration'])
        handler.addQuickElement(u'itunes:explicit', item['explicit'])
        handler.addQuickElement(u'itunes:author', item['author'])
        handler.addQuickElement(u'itunes:image', attrs={"href":item['image']})


class LatestSermonsFeed(Feed):
    feed_type = iTunesPodcastsFeedGenerator
    title = "Living Hope Sermons"
    description = "The latest sermons preached at Living Hope."
    subtitle = description
    summary = description
    iTunes_name = u'Living Hope Sermons'
    iTunes_email = u'info@onelivinghope.com'
    iTunes_image_url = static('livinghope/living-hope.jpg')
    iTunes_explicit = u'no'

    def link(self):
        return reverse(views.sermon_series)

    def feed_extra_kwargs(self, obj):
        return {'iTunes_name': self.iTunes_name,
                'iTunes_email': self.iTunes_email,
                'iTunes_image_url': self.iTunes_image_url,
                'iTunes_explicit': self.iTunes_explicit}


    def item_extra_kwargs(self, item):
        audio = MP3(item.recording.path)
        duration = audio.info.length
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        thumbnailer = get_thumbnailer(item.sermon_series.series_image)
        thumbnailer_options = {'size':(500, 500), 'background':'white', 'upscale':True}
        image = thumbnailer.get_thumbnail(thumbnailer_options).url

        return {'author': item.author.full_name(),
                'duration': '%d:%02d:%02d' % (h, m, s),
                'explicit': u'no',
                'image': image}

    def items(self):
        return Sermon.objects.all().exclude(recording='').order_by('-sermon_date')[:5]

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

    def item_pubdate(self, item):
        return datetime.combine(item.sermon_date, time())
    item_enclosure_mime_type = 'audio/mpeg'

