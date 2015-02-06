# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from livinghope.models import SermonSeries, Sermon, Author, BannerImage
from livinghope.models import Missionary, Leader, SmallGroup, Service
from livinghope.models import PrayerMeeting, Location, BlogPost, BlogTag
from livinghope.models import SpecialEvent, Ministry, LeadershipRole
from livinghope.models import MissionsPrayerMonth, ChildrensMinistryTeacher
from livinghope.models import ChildrensMinistryClass, Verse

from livinghope.forms import PrayerForm, ContactForm, ContactLeaderForm, SearchVerseForm
from livinghope.functions import parse_string_to_verses, test_parsable
from django.core.mail import send_mail
from aggregate_if import Count as CountIf


# from livinghope_proj.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
import math
import pickle
import datetime
# import paypalrestsdk

MONTHS = {1: 'January',
          2: 'February',
          3: 'March',
          4: 'April',
          5: 'May',
          6: 'June',
          7: 'July',
          8: 'August',
          9: 'September',
          10: 'October',
          11: 'November',
          12: 'December'}

# def paypal_create(request):

#     paypalrestsdk.configure({
#         "mode": PAYPAL_MODE,
#         "client_id": PAYPAL_CLIENT_ID,
#         "client_secret": PAYPAL_CLIENT_SECRET })

#     payment = paypalrestsdk.Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal" },
#         "redirect_urls": {
#             "return_url": request.build_absolute_uri(reverse('paypal_execute')),
#             "cancel_url": request.build_absolute_uri(reverse('giving')) },
#         "transactions": [{
#             "item_list": {
#                 "items": [{
#                     "name": "Donation",
#                     "price": "1",
#                     "currency": "USD",
#                     "quantity": 1 }]},
#             "amount":  {
#                 "total": "1",
#                 "currency": "USD" },
#             "description": "donation description" }]})

#     redirect_url = ""

#     if payment.create():
#         # Store payment id in user session
#         request.session['payment_id'] = payment.id

#         # Redirect the user to given approval url
#         for link in payment.links:
#             if link.method == "REDIRECT":
#                 redirect_url = link.href
#         return HttpResponseRedirect(redirect_url)

#     else:
#         messages.error(request, 'We are sorry but something went wrong. We could not redirect you to Paypal.')
#         return HttpResponseRedirect(reverse('home'))

# def paypal_execute(request):
#     """
#     MyApp > Paypal > Execute a Payment
#     """
#     payment_id = request.session['payment_id']
#     payer_id = request.GET['PayerID']

#     paypalrestsdk.configure({
#         "mode": PAYPAL_MODE,
#         "client_id": PAYPAL_CLIENT_ID,
#         "client_secret": PAYPAL_CLIENT_SECRET })

#     payment = paypalrestsdk.Payment.find(payment_id)
#     payment_name = payment.transactions[0].item_list.items[0].name

#     if payment.execute({"payer_id": payer_id}):
#         # the payment has been accepted
#         messages.success(request, 'thanks for the money dawg!')
#     else:
#         # the payment is not valid
#         messages.success(request, 'thanks for nothing!!!')
#     import pdb; pdb.set_trace()
#     return HttpResponseRedirect(reverse('home'))

def paginate(request, queryset, num_per_page):
    paginator = Paginator(queryset, num_per_page)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return queryset

def queryset_to_rows(queryset, num_cols):
    """
    helper function that accepts a queryset and returns
    the objects in the queryset broken up into rows
    of num_cols
    returns [row[obj, obj, obj...], [...]]
    """
    #stupid way of doing this
    #divide series into groups of three
    temp_holder = []
    all_objects_list = list(queryset) #force evaluation
    #below of hte form [row[series, series, series], [...]]
    all_objects_in_rows = []
    while all_objects_list:
        temp_holder.append(all_objects_list.pop(0))
        if len(temp_holder) == num_cols or not all_objects_list:
            all_objects_in_rows.append(temp_holder)
            temp_holder = []
    return all_objects_in_rows

def home(request):
    # banner_images = BannerImage.objects.all().order_by('order')
    today = datetime.datetime.today()
    # date_cutoff = today + datetime.timedelta(days=60)
    upcoming_events = SpecialEvent.objects.select_related('location').filter(
                                display_on_home_page=True,
                                display_on__lte=today,
                                date__gte=today
                            )
    headline = BlogPost.objects.filter(tags__name="News and Announcements").order_by(
                '-created_on')[0]
    
    news = BlogPost.objects.filter(tags__name="News and Announcements").exclude(
                id=headline.id).order_by(
                    '-created_on')[:5]

    latest_posts = BlogPost.objects.select_related('author').all().order_by('-created_on')[:3]

    context = {'upcoming_events':upcoming_events,
               'news': news, 'headline': headline,
               'latest_posts': latest_posts}
    return render(request, 'home.html', context)

def missions(request):
    missions_ministry = Ministry.objects.get(name='Missions')
    ministry_leaders = LeadershipRole.objects.filter(
                            ministry=missions_ministry,
                            primary_leader=True,
                            leader__active=True
                        ).select_related('leader')
    missionaries = Missionary.objects.all().order_by('last_name')
    rows_of_missionaries = queryset_to_rows(missionaries, 3)
    context = {'rows_of_missionaries': rows_of_missionaries,
               'missionaries': missionaries,
               'ministry_leaders': ministry_leaders}
    return render(request, 'missions.html', context)

def missions_partners(request):
    missions_ministry = Ministry.objects.get(name='Missions')
    ministry_leaders = LeadershipRole.objects.filter(
                            ministry=missions_ministry,
                            primary_leader=True,
                            leader__active=True
                        ).select_related('leader')
    missionaries = Missionary.objects.all().order_by('last_name')
    context = {'missionaries': missionaries,
               'ministry_leaders': ministry_leaders}
    return render(request, 'missions_partners.html', context)

def missionary_profile(request, missionary_id):
    try:
        missionary = Missionary.objects.get(id=missionary_id)
    except: #add specific exception later
        raise Http404
    context = {'missionary': missionary}
    return render(request, 'missionary_profile.html', context)

def events(request):
    now = datetime.datetime.now()
    events = SpecialEvent.objects.filter(
                    date__gte=now
                ).prefetch_related(
                    'organizer'
                ).order_by('date')

    events = paginate(request, events, 3)

    context = {'events':events}
    return render(request, 'events.html', context)

def leaders(request):
    #ORDER BY ORDER!!!!!
    leaders = Leader.objects.filter(
                    active=True
                ).prefetch_related(
                    'leadershiprole_set',
                    'leadershiprole_set__ministry',
                    'ministries'
                ).order_by('order','last_name')
    #get leaders into rows of two
    #depending on formatting, maybe don't need rows
    #consider modal? just thumnails of htem and then ajax modal 
    #for details??
    rows_of_leaders = queryset_to_rows(leaders, 2)
    ministries = Ministry.objects.all().order_by('name')
    context = {'rows_of_leaders': rows_of_leaders, 'all_leaders': leaders, 
               'ministries':ministries}
    return render(request, 'leaders.html', context)

def sermon_series(request, series_id=None):
    all_series = SermonSeries.objects.all().order_by('-start_date')
    searched = False
    if 'query' in request.GET: # this is if something was searched for
        searched = True
        form = SearchVerseForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd['query']
            verse_ids = parse_string_to_verses(query)
            verse_ids = list(set(verse_ids))
            #gets queryset of all songs that have a verse tag in the verse search list
            sermons = Sermon.objects.filter(
                                verses__id__in=verse_ids
                            ).distinct().annotate(
                                verse_matches=CountIf('verses', only=Q(verses__id__in=verse_ids))
                            ).select_related(
                                'author', 'sermon_series'
                            ).order_by('-verse_matches') #[:2] limits to 2
            # sermons = sermons.prefetch_related('authors', 'publisher')
            sermons = paginate(request, sermons, 20)
            
            #no longer needs just songs context element
            return render(request, 'sermons.html', {'sermons': sermons,
                'form':form, 'query':query,'all_series': all_series,})

    if series_id: #this is if a sermon series was selected
        try:
            series = SermonSeries.objects.get(id=int(series_id))
        except ObjectDoesNotExist:
            raise Http404
        #current series are put latest first but completed series
        #ordered by earliest first
        if series.current_series:
            sermons = series.sermon_set.all().select_related('author').order_by('-sermon_date')
        else:
            sermons = series.sermon_set.all().select_related('author').order_by('sermon_date')

        sermons = paginate(request, sermons, 20)
            
        context = {'sermons': sermons,
                    'all_series': all_series,
                    'series':series,}
        if searched:
            context.update({'form': form})
        return render(request, 'sermons.html', context)
    else: #this is to display all sermon series

        context = {'all_series':all_series}
        if searched:
            context.update({'form': form})
        return render(request, 'sermon_series.html', context)

class Prayer(FormView):
    template_name = 'prayer_form.html'
    form_class = PrayerForm
    success_url = reverse_lazy('prayer')

    def get_context_data(self, **kwargs):
        context = super(Prayer, self).get_context_data(**kwargs)
        context['prayer_meetings'] = PrayerMeeting.objects.all()
        return context

    def form_valid(self, form):
        form.send_prayer_email()
        success_message = "Thanks for submitting your prayer request! \
                            We will be praying!"

        messages.success(self.request, success_message)
        return super(Prayer, self).form_valid(form)

def paypal_payment_info_receiver(request):
    #this is where notify_url from a paypal button redirects to
    # implement this if we want to save basic payment info
    # only sent if user chooses to come back to the site after transaction though
    # unreliable
    print request

class Contact(FormView):
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super(Contact, self).get_context_data(**kwargs)
        context['locations'] = Location.objects.filter(church=True, public=True)
        return context

    def form_valid(self, form):
        form.send_contact_email()
        success_message = "Thanks for submitting your message!"
        messages.success(self.request, success_message)
        return super(Contact, self).form_valid(form)



#handling this in an AJAXy way. split it up into get and process
#so i don't have to use GET vs POST and worry about CSRF. Don't really understand CSRF
# do i really even need to split this up? nothing is writing to the db
#----------------------------
# What i do here is in a .get jquery call, i get a contact form
# with leader and system_subject populated based on data attrs in jquery
# data attrs: leader-id, subject, target=#contact-leader
# Must also have .contact-leader-link class!!
# I get the html for the form and pass it back to jquery to load into a modal
# In the modal, when the user clicks submit, i submit an ajax request
# to process_contact_leader_form. If the form is not valid, send
# the html representation of the form with errors back.
# If hte form is valid, then send back empty request.
# In ajax success callback, test if it's an empty request of has the form
# if it has the form, update the modal to have the form with errors.
# This last part had to be done 'recursively' since i had to 
# initialize all handlers upon instantiation of the html tags
# All JS in contact_leader.js
def get_contact_leader_form(request):
    # this sends back a form with populated leader and system_subject
    # to be processed by a modal
    leader_id = request.GET.get('leader-id')
    try:
        leader = Leader.objects.get(id=leader_id)
    except:
        return Http404
    system_subject = request.GET.get('system-subject')
    initial = {'system_subject':system_subject, 'leader':leader}
    form = ContactLeaderForm(initial=initial)
    process_url = reverse('process_contact_leader_form')
    context = {'form':form, 'process_url':process_url}
    html = render_to_string('contact_leader_form.html',context)
    return HttpResponse(html)

def process_contact_leader_form(request):
    form = ContactLeaderForm(request.GET)
    if form.is_valid():
        leader = form.cleaned_data['leader']
        success_message = "Thanks for submitting your message! %s will be in\
                           touch with you soon!" % leader.first_name
        messages.success(request, success_message)
        form.send_contact_email()

    else:
        process_url = reverse('process_contact_leader_form')
        context = {'form':form, 'process_url':process_url}
        html = render_to_string('contact_leader_form.html',context)
        return HttpResponse(html)
    return HttpResponse()


def statement_of_faith(request):
    return render(request, 'statement_of_faith.html')

def services(request):
    services = Service.objects.all()
    try:
        current_series = SermonSeries.objects.get(current_series=True)
    except:
        current_series = None 
    context = {'services':services, 'current_series': current_series}
    return render(request, 'services.html', context)

def ministries(request): # not used
    #maybe put in sunday school classes and stuff here?
    return render(request, 'ministries.html')

def small_groups(request):
    sgs = SmallGroup.objects.filter(
                    active=True
                ).prefetch_related(
                    'smallgroupimage_set'
                ).order_by('region')

    sg_ministry = Ministry.objects.get(name="Small Groups")
    #this could be more than one
    sg_coordinator_roles = LeadershipRole.objects.select_related(
                                'leader'
                            ).filter(
                                ministry=sg_ministry,
                                primary_leader=True,
                                leader__active=True,
                            )
    context = {'sgs':sgs,
               'sg_coordinator_roles':sg_coordinator_roles}
    return render(request, 'small_groups.html', context)

def denomination(request):
    return render(request, 'denomination.html')


def get_archive_post_list():
    all_posts = BlogPost.objects.all().order_by('-created_on')
    #need list to preserve order for template generation
    #archive will be of the form [[year,month,num_posts], ....]
    #want dictionary to do quick lookup if year-month combination exists
    #archive_contents of the form {(year,month):index_in_archive...}
    #over_two_years_ago of the form [[year, num_posts]] to limit
    #listing in archive posts sidebar
    archive_contents = {}
    archive = []
    current_year = datetime.datetime.now().year
    first_day_last_year = datetime.date(current_year-1, 1, 1)
    posts_over_two_years = all_posts.filter(
                                created_on__lt=first_day_last_year).values_list(
                                    'created_on', flat=True)
    #for posts over two years ago, only break down by year
    over_two_years_ago = []
    year_contents ={}
    for post_date in posts_over_two_years:
        year = post_date.year
        if year in year_contents:
            index = year_contents.get(year)
            over_two_years_ago[index][1] +=1
        else:
            over_two_years_ago.append([year, 1])
            index = len(over_two_years_ago) -1
            year_contents[year] = index

    #for posts in hte last two years, break it down by months
    posts_last_two_years = all_posts.filter(
                                created_on__gte=first_day_last_year).values_list(
                                    'created_on', flat=True)
    # archived_post_dates = all_posts.values_list('created_on', flat=True)

    for post_date in posts_last_two_years:
        year = post_date.year
        month = post_date.strftime("%B") #format month as name instead of int
        month_ordinal = post_date.month
        #if the year-month combo is already in the list
        #increment num_posts
        if (year, month) in archive_contents:
            index = archive_contents.get((year,month))
            archive[index][3] += 1
        else:
            #otherwise initialize in list and add year-month combo
            #to dictionary with value as index in archive list
            archive.append([year, month, month_ordinal, 1])
            index = len(archive) - 1
            archive_contents[(year,month)] = index
    return archive, over_two_years_ago

#class based view for blogs
class Blog(TemplateView):
    #all blog pages subclass from this
    #supplement get_context_data making sure to call super()
    # override template_name
    def paginate_blog(self, posts_queryset, num_per_page=5):
        """
        Pass in the queryset of posts you want
        Returns pagination
        Pass in num_per_page to defined how many posts per page
        """
        posts = paginate(self.request, posts_queryset, num_per_page)
        return posts

    def get_context_data(self):
        most_recent_posts = BlogPost.objects.all().order_by('-created_on')[:5].values(
                                'id', 'title', 'created_on')
        tags = BlogTag.objects.all().order_by('name') 
        published_author_ids = BlogPost.objects.all().values_list(
                                        'author', flat=True
                                    )
        #consider making this a method
        monthly_archive, yearly_archive = get_archive_post_list()
        published_authors = Author.objects.filter(
                                id__in=published_author_ids).values(
                                    'id','first_name', 'last_name'
                                )
        context = {'monthly_archive': monthly_archive,
                   'yearly_archive': yearly_archive,
                   'most_recent_posts': most_recent_posts,
                   'published_authors': published_authors,
                   'tags':tags
                   }
        return context

class BlogHome(Blog):
    template_name = 'blog.html'

    def get_context_data(self):
        context = super(BlogHome, self).get_context_data()
        all_posts = BlogPost.objects.all().order_by('-created_on')
        posts = self.paginate_blog(all_posts)
        context.update({'posts':posts, 
                        'page_title':'From the desk of Living Hope'})
        return context

class BlogMonth(Blog):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogMonth, self).get_context_data()
        month = int(kwargs.get('month'))
        year = int(kwargs.get('year'))
        month_name = MONTHS.get(month)
        if not month_name:
            raise Http404 #will this work?
        posts_in_month = BlogPost.objects.filter(
                                created_on__year=year,
                                created_on__month=month
                            ).order_by('created_on')
        posts = self.paginate_blog(posts_in_month)
        page_title = "Posts in %s, %d" % (month_name, year)
        unique_context = {'page_title': page_title,
                          'posts':posts}
        context.update(unique_context)
        return context

class BlogYear(Blog):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogYear, self).get_context_data()
        year = int(kwargs.get('year'))
        posts_in_year = BlogPost.objects.filter(created_on__year=year).order_by(
                                                'created_on')
        posts = self.paginate_blog(posts_in_year)
        page_title = 'Posts in %d' % year
        unique_context = {'page_title': page_title,
                          'posts':posts}
        context.update(unique_context)
        return context    

class BlogByTag(Blog):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogByTag, self).get_context_data()
        tag_id = kwargs.get('tag_id')
        tag = get_object_or_404(BlogTag, id=tag_id)
        posts = BlogPost.objects.filter(tags=tag).order_by('-created_on')
        posts = self.paginate_blog(posts)
        page_title = 'Posts tagged with %s' % tag
        unique_context = {'page_title':page_title,
                          'posts':posts}
        context.update(unique_context)
        return context  

class BlogSearch(Blog):
    template_name = 'blog.html'

    # this checks if the query is empty of has the placeholder
    # if so, then redirect to blog home
    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if not query or query=='Search...':
            return HttpResponseRedirect(reverse('blog'))
        else:
            return super(BlogSearch, self).dispatch(request, *args, **kwargs)

    def get_context_data(self):
        context = super(BlogSearch, self).get_context_data()
        #when given as a url param, in request
        #when parsed from the url itself, then in kwargs
        query = self.request.GET.get('query')
        by_content = Q(content__icontains=query)
        by_title = Q(title__icontains=query)
        #ordering??
        posts = BlogPost.objects.filter(by_content|by_title)
        posts = self.paginate_blog(posts)
        page_title = 'Resulting Posts for "%s"' % query
        unique_context = {'page_title':page_title,
                          'posts':posts}
        context.update(unique_context)
        return context

class BlogEntry(Blog):
    # this is the only one that can have a unique template
    template_name = 'blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogEntry, self).get_context_data()
        post_id = kwargs.get('post_id')
        post = get_object_or_404(BlogPost,id=post_id)
        #consider putting these also as methods
        try:
            previous_post_id = post.get_previous_by_created_on().id
        except:
            previous_post_id = None
        try:
            next_post_id = post.get_next_by_created_on().id
        except:
            next_post_id = None        

        unique_context = {'next_post_id':next_post_id,
                          'post':post,
                          'previous_post_id':previous_post_id}
        context.update(unique_context)
        return context

class BlogByAuthor(Blog):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogByAuthor, self).get_context_data()
        author_id = kwargs.get('author_id')
        author = get_object_or_404(Author, id=author_id)
        posts = BlogPost.objects.filter(author=author).order_by('-created_on')
        posts = self.paginate_blog(posts)
        page_title = 'Posts by %s' % author
        unique_context = {'page_title':page_title,
                          'posts':posts}
        context.update(unique_context)
        return context

def childrens_ministry(request):
    # add order
    childrens_ministry = Ministry.objects.get(name="Children's Ministry")
    classes = ChildrensMinistryClass.objects.all().order_by('order')
    ministry_leaders = LeadershipRole.objects.filter(
                            ministry=childrens_ministry,
                            primary_leader=True,
                            leader__active=True
                        )
    context = {'classes':classes, 
               'childrens_ministry': childrens_ministry, # good for ministry description
               'ministry_leaders': ministry_leaders
               }
    return render(request, 'childrens_ministry.html', context)

def prayer_calendar(request):
    prayer_months = MissionsPrayerMonth.objects.all().order_by('-year', '-month')

    prayer_months = paginate(request, prayer_months, 12)
    context = {'prayer_months': prayer_months}
    return render(request, 'missions_prayer_calendar.html', context)    

def load_sermons(request):
    #sermon_series_key links old id (key) to new id (value) 
    sermon_series_key = {2: 7,    #'new beginnings',
                         5: 6,    #'pause',
                         6: 5,    #'gripped'
                         7: 4,    #'further in',
                         8: 3,    #'healthy',
                         9: 2,    #'pulled',
                         10:8,    #'backto',
                         11:10,    #'hopeforliving',
                         12:9,    # 'grace pursuit',
                         13:11,    # 'building',
                         14:16,    # 'tragedy',
                         15:13,    #'born',
                         16:12,    #'encounters',
                         17:15,    #'standalone',
                         18:14,    # 'retreat',
                         19:1,    # 'servant'
                          }
    f = open('D:/dropbox/django/livinghope_proj/old_site_data.pickle', 
                'rb')
    sermons = pickle.load(f)
    f.close()
    g = open('D:/dropbox/django/livinghope_proj/failed_upload.txt', 
                'wb')
    for index, sermon in enumerate(sermons):
        title = sermon['title']
        passage = sermon['passage']
        date = sermon['date']
        try:
            author_first_last = sermon['author'].split(' ')
            author_first = author_first_last[0]
            author_last = author_first_last[1]
            author, created = Author.objects.get_or_create(
                                    first_name=author_first,
                                    last_name=author_last)
        except:
            author, created = Author.objects.get_or_create(
                                    first_name='placeholder',
                                    last_name='placeholder')

        series_id = sermon_series_key[int(sermon['series'])]
        series = SermonSeries.objects.get(id=series_id)

        transcript = sermon['transcript']
        if sermon['audiourl']:
            recording_path = 'sermon_recordings/%s.mp3' % date.strftime('%m%d%y')
        else:
            recording_path = ''
        sermon_obj = Sermon(sermon_date=date,
                            author=author,
                            title=title,
                            passage=passage,
                            sermon_series=series,
                            recording=recording_path,
                            manuscript=transcript.encode("utf8"))
        # print index, sermon_obj.title
        try:
            sermon_obj.save()
        except:
            sermon_obj.manuscript = ''
            sermon_obj.save()
            g.write(title + '\n\n')
            g.write(transcript.encode("utf8")+'\n\n')
            g.write('-----------------\n\n')
            print '%s failed!!!' % sermon_obj.title
            continue
    g.close()
    return render(request, 'home.html')

def display_sermon_transcript(request):
    sermon_id = request.GET.get('sermon-id', None)
    if not sermon_id:
        return Http404
    sermon = Sermon.objects.get(id=sermon_id)
    return HttpResponse(sermon.manuscript)

def report_broken_audio(request):
    sermon_id = request.GET.get('sermon-id', None)
    if not sermon_id:
        return Http404
    subject = "Living Hope - Broken sermon audio for id %s" % sermon_id
    body = "Please fix this broken audio"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
              settings.ADMIN_RECIPIENTS, fail_silently=False)
    success_message = "Thank you for caring enough to report the broken audio.\
                        Someone's been dispatched to fix it!"
    messages.success(request, success_message)
    return HttpResponse()

def display_event_details(request):
    # here is where the ajax call gets the html to fill the modal
    # for event details
    event_id = request.GET.get('event-id', None)
    try:
        event = SpecialEvent.objects.get(id=event_id)
    except:
        return Http404
    location = event.location
    organizers = event.organizer.all()
    context = {'event': event, 'location': location,
                'organizers': organizers}
    html = render_to_string('event_details_modal.html', context)
    return HttpResponse(html)



def giving(request):
    return render(request, 'giving.html')
