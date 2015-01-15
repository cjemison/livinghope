from django.contrib import admin
from django.db import models
from django import forms
from django.templatetags.static import static
from livinghope.models import Author, SermonSeries, Sermon, \
							  Location, Service, BannerImage, Missionary, \
							  Leader, PrayerMeeting, SmallGroup, BlogPost, \
                              BlogTag, SpecialEvent, MissionaryImage, Ministry, \
                              LeadershipRole

def set_leader_inactive(modeladmin, request, queryset):
    queryset.update(active=False)
set_leader_inactive.short_description = "Mark selected leaders as inactive"

def set_leader_active(modeladmin, request, queryset):
    queryset.update(active=True)
set_leader_active.short_description = "Mark selected leaders as active"

class MissionaryImageInline(admin.StackedInline):
    model = MissionaryImage

class MissionaryAdmin(admin.ModelAdmin):
    inlines = [MissionaryImageInline, ]


class SpecialEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'start_time', 'location')
    ordering = ('-date', '-start_time')
    filter_horizontal = ('organizer', )
    search_fields = ['name', 'location']

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

class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'sermon_date', 'author', 'sermon_series', 
                    'passage')
    ordering = ('-sermon_date',)
    search_fields = ['title', 'passage']

    # formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})},}
   
    # class Media:
    #     js = (static('livinghope/ckeditor/ckeditor.js'),)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on',)
    ordering = ('-updated_on', '-created_on')
    search_fields = ['title', 'content']
    filter_horizontal = ('tags', )

    # formfield_overrides = {models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})},}
   
    # class Media:
    #     js = (static('livinghope/ckeditor/ckeditor.js'),)

admin.site.register(Ministry)
admin.site.register(SpecialEvent, SpecialEventAdmin)
admin.site.register(BlogTag)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Missionary, MissionaryAdmin)
admin.site.register(PrayerMeeting)
admin.site.register(SmallGroup)
admin.site.register(Leader, LeaderAdmin)
admin.site.register(Location)
admin.site.register(Service)
admin.site.register(BannerImage, BannerImageAdmin)
admin.site.register(Author)
admin.site.register(SermonSeries, SermonSeriesAdmin)
admin.site.register(Sermon, SermonAdmin)