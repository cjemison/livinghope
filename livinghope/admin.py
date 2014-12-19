from django.contrib import admin
from livinghope.models import Author, SermonSeries, Sermon, \
							  Location, Service, BannerImage, Missionary, \
							  Leader, PrayerMeeting, SmallGroup

admin.site.register(Missionary)
admin.site.register(PrayerMeeting)
admin.site.register(SmallGroup)
admin.site.register(Leader)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(BannerImage)
admin.site.register(Author)
admin.site.register(SermonSeries)
admin.site.register(Sermon)