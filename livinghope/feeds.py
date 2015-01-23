from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from livinghope.models import Sermon
import views
from django.core.urlresolvers import reverse

class LatestSermonsFeed(Feed):
    title = "Living Hope Sermons"
    link = "/sitenews/"
    description = "The latest two sermons preached at Living Hope."

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
