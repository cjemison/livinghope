from django.contrib import admin
from django.db import models
from django import forms
from django.templatetags.static import static
from livinghope.models import (Author, SermonSeries, Sermon,
        Location, Service, BannerImage, Missionary,
		Leader, PrayerMeeting, SmallGroup, BlogPost, 
        BlogTag, SpecialEvent, MissionaryImage, Ministry, 
        LeadershipRole, SmallGroupImage, ChildrensMinistryClass,
        ChildrensMinistryTeacher, MissionsPrayerMonth,
        Book, Chapter, Verse, MinistryDocument, EventDocument,
        SermonDocument, DonationPosting, DonationPostingImage
    )

def set_leader_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
set_leader_inactive.short_description = "Mark selected leaders as inactive"

def set_leader_active(modeladmin, request, queryset):
    queryset.update(active=True)
set_leader_active.short_description = "Mark selected leaders as active"

class MissionaryImageInline(admin.StackedInline):
    model = MissionaryImage

class DonationPostingAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'contact_name', 'contact_email',
            'active', 'approved'
        )
    ordering = ('-created_on',)
    search_fields = ['name', 'contact_name', 'contact_email']

class MissionaryAdmin(admin.ModelAdmin):
    inlines = [MissionaryImageInline, ]


class MinistryDocumentInline(admin.StackedInline):
    model = MinistryDocument

class MinistryAdmin(admin.ModelAdmin):
    inlines = [MinistryDocumentInline, ]

class SmallGroupImageInline(admin.StackedInline):
    model = SmallGroupImage

class SmallGroupAdmin(admin.ModelAdmin):
    inlines = [SmallGroupImageInline, ]

class ChildrensMinistryClassAdmin(admin.ModelAdmin):
    list_display = ('youngest', 'oldest', 'order')
    ordering = ('order',)
    filter_horizontal = ('teachers',)


class EventDocumentInline(admin.StackedInline):
    model = EventDocument

class SpecialEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time', 'location')
    ordering = ('-date', '-start_time')
    filter_horizontal = ('organizer', )
    search_fields = ['name', 'location']
    fieldsets = (
        ('Starting At', 
            {
               'fields': ('start_time', 'day', 'date'),
            }
        ),
        ('Ending At', 
            {
                'fields': ('end_time', 'end_date'),
            }
        ),
        ('Main Info', 
            {
                'fields': ('name', 'main_image', 'organizer',
                            'location',
                            'description'
                            )
            }
        ),
        ('Home Page Automatic Display',
            {
                'fields': ('display_on_home_page', 'display_on',
                            'home_page_image',
                          )
            }
        )
    )
    inlines = [EventDocumentInline,]

class BannerImageAdmin(admin.ModelAdmin):
    list_display = ( 'name','order', 'image')
    ordering = ('order',)

class LeadershipRoleInline(admin.StackedInline):
    model = LeadershipRole


class LeaderAdmin(admin.ModelAdmin):
    list_display = ( 'first_name', 'last_name', 'order','active')
    ordering = ('order',)
    inlines = [LeadershipRoleInline, ]
    actions = [set_leader_inactive, set_leader_active]

class SermonSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'passage_range', 'start_date', 'end_date',
                    'current_series')
    ordering = ('-start_date',)

class SermonDocumentInline(admin.StackedInline):
    model = SermonDocument

class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'sermon_date', 'author', 'sermon_series', 
                    'passage')
    ordering = ('-sermon_date',)
    search_fields = ['title', 'passage']
    exclude = ('verses', )
    inlines = [SermonDocumentInline,]

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on',)
    ordering = ('-updated_on', '-created_on')
    search_fields = ['title', 'content']
    filter_horizontal = ('tags', )


class MissionsPrayerMonthAdmin(admin.ModelAdmin):
    list_display = ('highlight', 'month', 'year')
    ordering = ('-year', '-month')
    search_fields = ['highlight',]

# admin.site.register(Book)
# admin.site.register(Chapter)
# admin.site.register(Verse)
admin.site.register(DonationPosting, DonationPostingAdmin)
admin.site.register(MissionsPrayerMonth, MissionsPrayerMonthAdmin)
admin.site.register(ChildrensMinistryClass, ChildrensMinistryClassAdmin)
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(SpecialEvent, SpecialEventAdmin)
admin.site.register(BlogTag)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Missionary, MissionaryAdmin)
admin.site.register(PrayerMeeting)
admin.site.register(SmallGroup, SmallGroupAdmin)
admin.site.register(Leader, LeaderAdmin)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(BannerImage, BannerImageAdmin)
admin.site.register(Author)
admin.site.register(SermonSeries, SermonSeriesAdmin)
admin.site.register(Sermon, SermonAdmin)