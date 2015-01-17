# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from livinghope.models import SermonSeries, Sermon, Author, BannerImage
from livinghope.models import Missionary, Leader, SmallGroup, Service
from livinghope.models import PrayerMeeting, Location, BlogPost, BlogTag
from livinghope.models import SpecialEvent, Ministry, LeadershipRole

from livinghope.forms import PrayerForm, ContactForm
from django.core.mail import send_mail
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
    banner_images = BannerImage.objects.all().order_by('order')
    headline = BlogPost.objects.filter(tags__name="News and Announcements").order_by(
                '-created_on')[0]
    
    news = BlogPost.objects.filter(tags__name="News and Announcements").exclude(
                id=headline.id).order_by(
                    '-created_on')[:5]

    latest_posts = BlogPost.objects.all().order_by('-created_on')[:3]

    context = {'banner_images': banner_images,
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

def missionary_profile(request, missionary_id):
    try:
        missionary = Missionary.objects.get(id=missionary_id)
    except: #add specific exception later
        raise Http404
    context = {'missionary': missionary}
    return render(request, 'missionary_profile.html', context)

def events(request):
    now = datetime.datetime.now()
    events = SpecialEvent.objects.filter(date__gte=now).order_by('date')
    context = {'events':events}
    return render(request, 'events.html', context)

def leaders(request):
    #ORDER BY ORDER!!!!!
    leaders = Leader.objects.filter(active=True).order_by('order','last_name')
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
    if series_id: #this is if a sermon series was selected
        try:
            series = SermonSeries.objects.get(id=int(series_id))
        except ObjectDoesNotExist:
            raise Http404
        sermons = series.sermon_set.all().order_by('-sermon_date')
        #paginate!
        paginator = Paginator(sermons, 20)
        page = request.GET.get('page')
        try:
            sermons = paginator.page(page)
        except PageNotAnInteger:
            sermons = paginator.page(1)
        except EmptyPage:
            sermons = paginator.page(paginator.num_pages)
            
        context = {'sermons': sermons,
                    'all_series': all_series,
                    'series':series,}
        return render(request, 'sermons.html', context)
    else: #this is to display all sermon series
        all_series_in_rows = queryset_to_rows(all_series, 3)

        context = {'all_series_in_rows': all_series_in_rows, 'all_series':all_series}
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


def statement_of_faith(request):
    return render(request, 'statement_of_faith.html')

def services(request):
    services = Service.objects.all()
    context = {'services':services}
    return render(request, 'services.html', context)

def ministries(request):
    #maybe put in sunday school classes and stuff here?
    return render(request, 'ministries.html')

def denomination(request):
    return render(request, 'denomination.html')

#refactor blog portion into class based view?
def blog(request):
    # all_posts = BlogPost.objects.all().order_by('-created_on')
    # most_recent_posts = all_posts[:5]
    all_posts = BlogPost.objects.all().order_by('-created_on')
    most_recent_posts = all_posts[:5].values(
                            'title', 'id', 'created_on')
    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')
    tags = BlogTag.objects.all().order_by('name')
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    monthly_archive, yearly_archive = get_archive_post_list()
    # all_post_data = all_posts.values('title', 'created_on')
    context = {'most_recent_posts': most_recent_posts,
               'monthly_archive': monthly_archive,
               'yearly_archive': yearly_archive,
               'all_posts': all_posts,
               'tags':tags}
    return render(request, 'blog.html', context)

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

def blog_by_month(request, year, month):
    month = int(month)
    year = int(year)
    month_name = MONTHS.get(month)
    if not month_name:
        return Http404
    #paginate??
    tags = BlogTag.objects.all().order_by('name')
    posts_in_month = BlogPost.objects.filter(created_on__year=year,
                                             created_on__month=month).order_by(
                                                'created_on')
    paginator = Paginator(posts_in_month, 5)
    page = request.GET.get('page')
    try:
        posts_in_month = paginator.page(page)
    except PageNotAnInteger:
        posts_in_month = paginator.page(1)
    except EmptyPage:
        posts_in_month = paginator.page(paginator.num_pages)

    most_recent_posts = BlogPost.objects.all().order_by('-created_on')[:5].values(
                                'id', 'title', 'created_on')
    monthly_archive, yearly_archive = get_archive_post_list()
    context = {'posts_in_month': posts_in_month,
               'monthly_archive': monthly_archive,
               'yearly_archive': yearly_archive,
               'month_name': month_name,
               'year': year,
               'most_recent_posts': most_recent_posts,
               'tags':tags}
    return render(request, 'blog_by_month.html', context)

def blog_by_year(request, year):
    year = int(year)
    posts_in_year = BlogPost.objects.filter(created_on__year=year).order_by(
                                                'created_on')
    paginator = Paginator(posts_in_year, 5)
    page = request.GET.get('page')
    tags = BlogTag.objects.all().order_by('name')
    try:
        posts_in_year = paginator.page(page)
    except PageNotAnInteger:
        posts_in_year = paginator.page(1)
    except EmptyPage:
        posts_in_year = paginator.page(paginator.num_pages)

    most_recent_posts = BlogPost.objects.all().order_by('-created_on')[:5].values(
                                'id', 'title', 'created_on')
    monthly_archive, yearly_archive = get_archive_post_list()
    context = {'posts_in_year': posts_in_year,
               'monthly_archive': monthly_archive,
               'yearly_archive': yearly_archive,
               'year': year,
               'most_recent_posts': most_recent_posts,
               'tags': tags}
    return render(request, 'blog_by_year.html', context)


def blog_entry(request, blog_id):
    try:
        post = BlogPost.objects.get(id=blog_id)
    except:
        return Http404
    try:
        previous_post_id = post.get_previous_by_created_on().id
    except:
        previous_post_id = None
    try:
        next_post_id = post.get_next_by_created_on().id
    except:
        next_post_id = None 
    tags = BlogTag.objects.all().order_by('name')
    all_posts = BlogPost.objects.all().order_by('-created_on')
    most_recent_posts = all_posts[:5].values('id', 'title', 'created_on')

    monthly_archive, yearly_archive = get_archive_post_list()

    context = {'post':post, 'next_post_id':next_post_id,
                'previous_post_id': previous_post_id,
                'most_recent_posts': most_recent_posts,
                'monthly_archive': monthly_archive,
                'yearly_archive': yearly_archive,
                'tags':tags}
    return render(request, 'blog_post.html', context)

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
    send_mail(subject, body, 'prayer@onelivinghope.com',
              ['rhsiao2@gmail.com'], fail_silently=False)
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