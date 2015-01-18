from django.db import models
from ckeditor.fields import RichTextField
from geopy.geocoders import GoogleV3


class Person(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75, blank=True, null=True)
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        abstract = True

class Missionary(Person):
    class Meta:
        verbose_name_plural = "Missionaries"

    profile_picture = models.ImageField(upload_to='./missionary_images/',
                                blank=True,
                                null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)

    def __unicode__(self):
        if self.organization:
            return "%s %s with %s" % (self.first_name, 
                                  self.last_name,
                                  self.organization)
        return "%s %s" % (self.first_name, 
                                  self.last_name)

class MissionaryImage(models.Model):
    image = models.ImageField(upload_to='./missionary_images/')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=100, blank=True, null=True)
    missionary = models.ForeignKey(Missionary)
    order = models.IntegerField(max_length=2, default=0)

    #add clean to deal with order

    def __unicode__(self):
        return '%s for %s' % (self.title, self.missionary)

class Author(Person):

    def __unicode__(self):
        return self.full_name()

class Ministry(models.Model):
    class Meta:
        verbose_name_plural = "Ministries"
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Leader(Person):
    profile_picture = models.ImageField(upload_to='./leader_images/',
                                blank=True,
                                null=True)
    ministries = models.ManyToManyField(Ministry, through="LeadershipRole",)
    active = models.BooleanField(default=True)
    bio = RichTextField(blank=True, null=True)
    order = models.IntegerField(max_length=2, default=0)

    def save(self):
        #make sure there are no repeats in order.
        #if encountering another leader with same order, then push them 
        #down in order
        past_leader_in_order = Leader.objects.filter(order=self.order)
        #prevent issue where the past_leader_in_order was itself
        if past_leader_in_order and past_leader_in_order[0].id != self.id:
            past_leader_obj = past_leader_in_order[0]
            past_leader_obj.order = self.order+1
            past_leader_obj.save()
        super(Leader, self).save()

class LeadershipRole(models.Model): #rename this roles?
    leader = models.ForeignKey(Leader)
    ministry = models.ForeignKey(Ministry)
    special_name = models.CharField(max_length=100, blank=True, null=True)
    primary_leader = models.BooleanField(default=False)

class BlogTag(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name

class BlogPost(models.Model):
    main_image = models.ImageField(upload_to='./blog_main_images/',
                                    blank=True,
                                    null=True,
                                    help_text="For best results, the width of the image \
                                                should be larger than the height. Ideally \
                                                5:3 aspect ratio")
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(BlogTag, blank=True, null=True)
    content = RichTextField()

    def clean(self):
        #remove <p>&nbsp;</p> from manuscripts
        self.content = self.content.replace('<p>&nbsp;</p>', '')
        super(BlogPost, self).clean()

class BannerImage(models.Model):
    name = models.CharField(max_length=25, blank=True, null=True)
    image = models.ImageField(upload_to='./banner_images/',
                                blank=True,
                                null=True)
    order = models.IntegerField(max_length=2)
    #must be hardcoded pretty much UGH!!!
    link_to = models.CharField(max_length=100, blank=True, null=True, default='#')

    def save(self):
        #make sure there are no repeats in order.
        #if encountering another bannerimage with same order, then push them 
        #down in order
        past_banner_in_order = BannerImage.objects.filter(order=self.order)
        if past_banner_in_order:
            past_banner_obj = past_banner_in_order[0]
            past_banner_obj.order = self.order+1
            past_banner_obj.save()
        super(BannerImage, self).save()

    def __unicode__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)

    church = models.BooleanField(default=False)
    public = models.BooleanField(default=False, 
                                 help_text="Is this location's address OK to show publicly?")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self):
        #automatically get lat and lon if it doesn't exist and is public
        if not self.latitude and not self.longitude and self.public:
            full_address = '%s, %s, %s %s' % (self.street_address,
                                              self.city, self.state,
                                              self.zip_code)
            geolocator = GoogleV3()
            location = geolocator.geocode(full_address)
            self.latitude = location.latitude
            self.longitude = location.longitude
        super(Location, self).save()

    def __unicode__(self):
        return "%s - %s %s" % (self.name, self.city, self.state)

class SundaySchoolClass(models.Model):
    pass

class Event(models.Model):
    class Meta:
        abstract = True

    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUES', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    day = models.CharField(max_length=4, choices=DAYS_OF_WEEK,
                            default='SUN')
    location = models.ForeignKey(Location)

class SpecialEvent(Event):
    name = models.CharField(max_length=100)
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    organizer = models.ManyToManyField(Leader)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Service(Event):
    def __unicode__(self):
        return "%s service @ %s" % (self.location.name, self.start_time)


class SmallGroup(Event):
    leaders = models.ManyToManyField(Leader, null=True, blank=True)
    region = models.CharField(max_length=30)
    main_image = models.ImageField(upload_to='./small_group_images/',
                                    blank=True,
                                    null=True)
    description = RichTextField(null=True, blank=True)

    def __unicode__(self):
        return "%s Small Group" % self.region

class SmallGroupImage(models.Model):
    image = models.ImageField(upload_to='./small_group_images/')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=100, blank=True, null=True)
    small_group = models.ForeignKey(SmallGroup)
    order = models.IntegerField(max_length=2, default=0)

    #add clean to deal with order

    def __unicode__(self):
        return '%s for %s' % (self.title, self.small_group)


class PrayerMeeting(Event):
    def __unicode__(self):
        return "Prayer Meeting @ %s" % self.location.name

class SermonSeries(models.Model):
    class Meta:
        verbose_name_plural = "Sermon Series"
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100)
    #consider using django-filer in the future?
    series_image = models.ImageField(upload_to='./sermon_series/',
                                    blank=True,
                                    null=True)
    series_image_thumbnail = models.ImageField(upload_to='./sermon_series_thumb/',
                                               null=True)
    passage_range = models.CharField(max_length=50)
    current_series = models.BooleanField(default=False)
    description = RichTextField(blank=True, null=True)

    def clean(self):
        if self.current_series == True:
            previous_current = SermonSeries.objects.filter(current_series=True)
            previous_current.update(current_series=False)
        super(SermonSeries, self).clean()

    def __unicode__(self):
        return self.name

class Sermon(models.Model):
    sermon_date = models.DateField()
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    sermon_series = models.ForeignKey(SermonSeries)
    recording = models.FileField(upload_to='./sermon_recordings/')
    passage = models.CharField(max_length=50, 
                                blank=True,
                                null=True)
    manuscript = RichTextField(blank=True, null=True)

    # manuscript = models.TextField(blank=True, null=True)

    def clean(self):
        #remove <p>&nbsp;</p> from manuscripts
        self.manuscript = self.manuscript.replace('<p>&nbsp;</p>', '')
        super(Sermon, self).clean()

    def __unicode__(self):
        return "%s - %s by %s" % (str(self.sermon_date), 
                                    self.passage,
                                    self.author.full_name())

