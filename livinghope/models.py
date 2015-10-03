from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.db.models.fields.files import ImageFieldFile, ImageField
from django.template.loader import render_to_string

from ckeditor.fields import RichTextField
from geopy.geocoders import GoogleV3
class SmartImageFieldFile(ImageFieldFile):
    """
    This is an image file that, in addition to all the nice
    things django adds, will expose a method to calculate
    whether the image is landscape or portrait
    """
    def _is_wide(self):
        self._require_file()
        aspect_ratio = float(self.width)/self.height
        # of should this be 5:3?
        # show as landscape if aspect ratio of 2:1 or greater
        if aspect_ratio >= 1.66:
            return True
        return False

    def _is_landscape(self):
        self._require_file()
        if self.width > self.height:
            return True
        return False

    is_wide = property(_is_wide)
    is_landscape = property(_is_landscape)
    #this is where to put my method to calculate aspect ratio

class SmartImageField(ImageField):
    """
    An extremely thin wrapping around ImageField simply adding
    a hook into determining if an image should be displayed
    in landscape or portrait
    """
    attr_class = SmartImageFieldFile

class DonationPosting(models.Model):
    DONATION_TYPES = [(True, 'Seeking'),
            (False, 'Donating')]

    seeking = models.BooleanField(default=False, choices=DONATION_TYPES,
        verbose_name="Are you donating or seeking?")
    name = models.CharField(max_length=127, 
        verbose_name="What are you donating or looking for?")
    created_on = models.DateTimeField(auto_now_add=True)
    contact_name = models.CharField(max_length=127,
        verbose_name="What's your name?")
    #change this later
    contact_email = models.EmailField(max_length=254,
        verbose_name="What email should responses be sent to?")
    description = models.TextField(blank=True,
        verbose_name="Briefly describe what you are donating or looking for")
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    number_of_responses = models.IntegerField(default=0, max_length=3)

    def save(self):
        #hook into when admin approves donation posting
        if self.id:
            old_posting = DonationPosting.objects.get(pk=self.id)
            #changed from not approved to approved
            if old_posting.approved == False and self.approved == True:
                subscribers = DonationSubscriber.objects.filter(active=True)
                for subscriber in subscribers:
                    subscriber.send_email(self)
        return super(DonationPosting, self).save()

    def __unicode__(self):
        return "Donation of %s by %s (%s) on %s" % (self.name, 
                self.contact_name, self.contact_email, self.created_on
            )

    
class DonationPostingImage(models.Model):
    image = SmartImageField(upload_to='./donation_images/')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=127)
    donation_posting = models.ForeignKey('DonationPosting')

    def __unicode__(self):
        return self.title

class DonationSubscriber(models.Model):
    email = models.EmailField(max_length=75)
    active = models.BooleanField(default=True)

    def send_email(self, posting):
        #takes in a posting and sends out the email for it to subscriber
        subject = "A new donation has been posted on the LH website"
        domain = Site.objects.get(id=settings.SITE_ID).domain
        context = {'posting': posting, 
                'subscriber':self,
                'domain': domain}
        body = render_to_string('donation_subscriber_email.html', context)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
            [self.email], fail_silently=False)
        return

    def __unicode__(self):
        return self.email

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
    website = models.URLField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
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
    caption = models.CharField(max_length=255, blank=True, null=True)
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
    description = RichTextField(blank=True, null=True)

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
    special_name = models.CharField(max_length=255, blank=True, null=True)
    primary_leader = models.BooleanField(default=False)

class BlogTag(models.Model):
    name = models.CharField(max_length=40)

    def save(self):
        # force name to be title case
        self.name = self.name.title()
        super(BlogTag, self).save()

    def __unicode__(self):
        return self.name

class BlogPost(models.Model):
    main_image = SmartImageField(upload_to='./blog_main_images/',
                                    blank=True,
                                    null=True,
                                    help_text="For best results, the width of the image \
                                                should be larger than the height. Ideally \
                                                5:3 aspect ratio")
    title = models.CharField(max_length=255)
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
    link_to = models.CharField(max_length=255, blank=True, null=True, default='#')

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
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
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
    name = models.CharField(max_length=255)
    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    main_image = SmartImageField(upload_to='./event_images/',
                                    blank=True,
                                    null=True,
                                    help_text="This is the image that will be\
                                    displayed on the event page. NOT displayed on\
                                    the home page.")
    organizer = models.ManyToManyField(Leader,
                                       help_text="This is who the main point of contact\
                                       should be for this event.")
    display_on_home_page = models.BooleanField(
                                    default=False,
                                    help_text="Should this be shown on the \
                                    home page slider when the event approaches?"
                                )
    display_on = models.DateField(null=True, blank=True, 
                                  verbose_name="Display on home page on this date",
                                  )
    home_page_image = SmartImageField(upload_to='./event_images/',
                                    blank=True,
                                    null=True,
                                    help_text="This is the background image that\
                                    will be displayed on the homepage slider.<br>\
                                    This needs to be 1920x470 otherwise will look\
                                    strange.")

    description = RichTextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Service(Event):
    def __unicode__(self):
        return "%s service @ %s" % (self.location.name, self.start_time)


class SmallGroup(Event):
    leaders = models.ManyToManyField(Leader, null=True, blank=True,
                                     help_text="This is currently optional and will \
                                     not actually display publicly")
    region = models.CharField(max_length=30)
    main_image = SmartImageField(upload_to='./small_group_images/',
                                    blank=True,
                                    null=True,
                                    help_text="This image will be displayed at the top\
                                    of your small group section on the small groups page")
    description = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=True,
                                 help_text="Only small groups marked as active will be\
                                 displayed on the small groups page")
    def __unicode__(self):
        return "%s Small Group" % self.region

class SmallGroupImage(models.Model):
    image = models.ImageField(upload_to='./small_group_images/')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=255, blank=True, null=True)
    small_group = models.ForeignKey(SmallGroup)
    order = models.IntegerField(max_length=2, default=0)

    #add clean to deal with order

    def __unicode__(self):
        return '%s for %s' % (self.title, self.small_group)


class PrayerMeeting(Event):
    def __unicode__(self):
        return "Prayer Meeting @ %s" % self.location.name

class MissionsPrayerMonth(models.Model):
    MONTHS = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    main_image = SmartImageField(upload_to='./prayer_month_images/',
                                   blank=True, null=True, 
                                   help_text="This image will be displayed portrait-style\
                                              so landscape images will be cropped.")
    main_image_caption = models.CharField(blank=True,
                                          null=True,
                                          max_length=255,
                                          help_text="Brief description of the image")
    highlight = models.CharField(max_length=255, default='',
                                 help_text="What is being highlighted this month?")
    # missionary = models.ForeignKey(Missionary, blank=True, null=True,
    #                help_text='Put this in if the highlight is also a missionary we support')
    month = models.IntegerField(max_length=2, choices=MONTHS)
    year = models.IntegerField(max_length=4, help_text="Enter full year not just 15")
    prayer_requests = RichTextField()

    class Meta:
        unique_together = ('month', 'year')

    def __unicode__(self):
        return 'Prayer requests for %s, %s (%s)' % (self.month, self.year, self.highlight)

class ChildrensMinistryTeacher(Person):
    def __unicode__(self):
        return self.full_name()

class ChildrensMinistryClass(models.Model):
    main_image = SmartImageField(upload_to='./childrens_ministry_images/',
                                    null=True, blank=True)
    youngest = models.CharField(max_length=40,
                                help_text="What is the lower bound of the age range?")
    oldest = models.CharField(max_length=40, 
                              help_text="What is the upper bound of the age range?")
    teachers = models.ManyToManyField(ChildrensMinistryTeacher, 
                                      blank=True, null=True)
    order = models.IntegerField(max_length=2, default=0,
                                help_text="This determines the ordering of classes\
                                on the Children's ministry page.")
    description = RichTextField()

    def __unicode__(self):
        return 'Class from %s to %s' % (self.youngest, self.oldest)


class Book(models.Model):
    name = models.CharField(max_length=30)
    num_chapters = models.IntegerField(verbose_name='number of chapters')
    order_index = models.IntegerField(primary_key=True)
    
    def __unicode__(self):
        return self.name
    
class Chapter(models.Model):
    book = models.ForeignKey(Book)
    number = models.IntegerField(verbose_name="chapter")
    num_verses = models.IntegerField(verbose_name="number of verses")
    
    def __unicode__(self):
        return u'%s %s' % (self.book, self.number)
    
class Verse(models.Model):
    book = models.ForeignKey(Book)
    chapter = models.ForeignKey(Chapter)
    number = models.IntegerField()
    def __unicode__(self):
        return u'%s:%s' % (self.chapter,self.number)

class EventDocument(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='./event_documents/')
    event = models.ForeignKey(SpecialEvent)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.event)

class MinistryDocument(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='./ministry_documents/')
    ministry = models.ForeignKey(Ministry)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.ministry)

class SermonSeries(models.Model):
    class Meta:
        verbose_name_plural = "Sermon Series"
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=255)
    #consider using django-filer in the future?
    series_image = models.ImageField(upload_to='./sermon_series/',
                                     help_text="Image should be ideally\
                                                1500x1125 or 720x540")
    # series_image_thumbnail = models.ImageField(upload_to='./sermon_series_thumb/',
    #                                            null=True)
    homepage_image = models.ImageField(upload_to='./sermon_series_home/',
                                       help_text="This image is the one that\
                                              will be displayed on the home page when\
                                              this series is the current series. \
                                              Ideally this should be 1920x470",
                                       blank=True,
                                       null=True)
    passage_range = models.CharField(max_length=50)
    current_series = models.BooleanField(default=False,
                                         help_text="Is this the current series?")
    description = RichTextField(blank=True, null=True)

    def clean(self):
        if self.current_series == True:
            previous_current = SermonSeries.objects.filter(current_series=True)
            previous_current.update(current_series=False)
        super(SermonSeries, self).clean()

    def __unicode__(self):
        return self.name

class Sermon(models.Model):
    PASSAGE_HELP_TEXT = """
                        Do not abbreviate book names. Separate verses by commas
                        and always include chapter number if applicable.<br>
                        If the passage spans whole chapters, it's acceptable to 
                        separate chapter numbers with a "-" if book name is given.<br>
                        Good, very clear: Philippians 1:1-3, 1:6-8, 1 John 1 <br>
                        Bad, ambiguous: Phi. 1:1-3, 6-8. Is this Philippians or Philemon? 
                        6-8 would be interpreted as chapters 6-8 not verses 1:6-8
                        """
    sermon_date = models.DateField(help_text="When was the sermon preached?")
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author)
    sermon_series = models.ForeignKey(SermonSeries)
    recording = models.FileField(upload_to='./sermon_recordings/',
                                 null=True, blank=True)
    passage = models.CharField(max_length=50, 
                                blank=True,
                                null=True,
                                help_text = PASSAGE_HELP_TEXT)
    verses = models.ManyToManyField(Verse, blank=True)
    manuscript = RichTextField(blank=True, null=True)

    __original_passage = None

    def __init__(self, *args, **kwargs):
        #override this to check if passage has changed
        super(Sermon, self).__init__(*args, **kwargs)
        self.__original_passage = self.passage

    def clean(self):
        #remove <p>&nbsp;</p> from manuscripts
        self.manuscript = self.manuscript.replace('<p>&nbsp;</p>', '')
        super(Sermon, self).clean()

    def save(self):
        #Overriding save to parse passage into verse objects

        # import this here to avoid circular import
        from livinghope.functions import parse_string_to_verses

        # this is needed for the case where sermon is new object
        # must have object before establishgin M2M relationship
        super(Sermon, self).save()

        #if the passage has changed or first time initializing
        # also covers case where a sermon's passage hasn't been parsed to verses
        if self.passage:
            if self.__original_passage != self.passage or (self.passage and not self.verses.all()):
                self.verses.clear()
                try: #if there is an error in parsing, just quit
                    verse_list = parse_string_to_verses(self.passage)
                except:
                    return
                verses = Verse.objects.filter(id__in=verse_list)
                self.verses.add(*verses)
                super(Sermon, self).save()

    def __unicode__(self):
        return "%s - %s by %s" % (str(self.sermon_date), 
                                    self.passage,
                                    self.author.full_name())

class SermonDocument(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='./sermon_documents/')
    sermon = models.ForeignKey(Sermon)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s for %s' % (self.name, self.sermon)
