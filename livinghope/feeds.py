from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from livinghope.models import Sermon
import views
from mutagen.mp3 import MP3 # this is to find duration of recordings
from django.core.urlresolvers import reverse

class LatestSermonsFeed(Feed):
    title = "Living Hope Sermons"
    link = "/sitenews/"
    description = "The latest two sermons preached at Living Hope."

    iTunes_name = u'Living Hope Sermons'
    iTunes_email = u'info@onelivinghope.com'
    iTunes_image_url = u''
    iTunes_explicit = u'no'

    def feed_extra_kwargs(self, obj):
        return {'iTunes_name': self.iTunes_name,
                'iTunes_email': self.iTunes_email,
                'iTunes_image_url': self.iTunes_image_url,
                'iTunes_explicit': self.iTunes_explicit}

    def item_extra_kwargs(self, item):
        audio = MP3(item.path)
        duration = audio.info.length
        return {'author': item.author,
                'duration': duration,
                'explicit': u'no'}

    def author_name(self, item):
        return item.author

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
        return item.recording.size

    def item_pubdate(self, item):
        return item.sermon_date

    item_enclosure_mime_type = 'audio/mpeg'
    # def item_enclosure_mime_type(self, item):
