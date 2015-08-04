from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy, reverse
from captcha.fields import CaptchaField, CaptchaTextInput
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.conf import settings
from livinghope.models import (Leader, DonationPosting, DonationPostingImage,
        DonationSubscriber
    )
from livinghope.functions import test_parsable
# from django.utils.safestring import mark_safe

# class BootstrapCaptchaField(CaptchaField):
#     def __init__(self, *args, **kwargs):
#         super(CaptchaField, self).__init__()

class DonationSubscriberForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(
            attrs={'class':'form-control'}))
    class Meta:
        model = DonationSubscriber
        fields = ['email']
        widgets = {'email': forms.TextInput(attrs={'class':'form-control'})}

    def clean_email(self):
        #could do unique_on on the model but i want to have this reactivate
        #emails that have unsubscribed
        email = self.data.get('email')
        if email:
            #just get rid of the old subscriber object and allow
            #form to create a new one.
            subscribers = DonationSubscriber.objects.filter(email=email)
            subscribers.delete()
        return email

class DonationPostingForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(
            attrs={'class':'form-control'}))
    class Meta:
        model = DonationPosting
        fields = ['seeking', 'name', 'contact_name', 'contact_email', 
            'description']
        widgets = {'name': forms.TextInput(attrs={'class':'form-control'}),
            'contact_name': forms.TextInput(attrs={'class':'form-control'}),
            'contact_email': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'seeking': forms.Select(attrs={'class':'form-control'})
        }


class DonationPostingImageForm(forms.ModelForm):
    class Meta:
        model = DonationPostingImage
        fields = ['image', 'title']
        widgets = {
            # 'image': forms.FileInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'})
        }

    def save(self, donation_posting):
        cd = self.cleaned_data
        posting_image = DonationPostingImage(
                image=cd['image'], title=cd['title'],
                donation_posting=donation_posting
            )
        posting_image.save()

#In the future, use subclasses for contact forms
class DonationContactForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    your_email = forms.EmailField(label='Your Email', max_length=100,
                                  required=True,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
 
    your_message =  forms.CharField(label='Your Message', required=True,
                                widget=forms.Textarea(attrs={'class':'form-control'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class':'form-control'}))

    donation_posting = forms.ModelChoiceField(
            queryset=DonationPosting.objects.filter(active=True, approved=True),
            required=True,
            widget=forms.HiddenInput())

    def send_contact_email(self):
        name = self.cleaned_data.get('your_name', 'unknown sender')
        email = self.cleaned_data['your_email']
        message = self.cleaned_data['your_message']
        donation_posting = self.cleaned_data['donation_posting']

        subject = 'Living Hope donation posting response'
        donor_email = donation_posting.contact_email
        context = {'name':name, 'email': email,
                    'message':message, 'donation':donation_posting}
        body = render_to_string('contact_email_donation_template.html', context)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                 [donor_email], fail_silently=False)


class ContactForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    your_email = forms.EmailField(label='Your Email', max_length=100,
                                  required=True,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    your_message =  forms.CharField(label='Your Message', required=True,
                                widget=forms.Textarea(attrs={'class':'form-control'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class':'form-control'}))

    def send_contact_email(self):
        name = self.cleaned_data.get('your_name', 'unknown')
        email = self.cleaned_data['your_email']
        message = self.cleaned_data['your_message']
        
        subject = "Living Hope message from %s" % name
        context = {'name':name, 'email': email,
                    'message':message}
        body = render_to_string('contact_email_template.html', context)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                 settings.EMAIL_RECIPIENTS, fail_silently=False)

class ContactLeaderForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    your_email = forms.EmailField(label='Your Email', max_length=100,
                                  required=True,
                                  widget=forms.TextInput(attrs={'class':'form-control'}))
    subject = forms.CharField(label='Subject', max_length=50,
                              required=True,
                              widget=forms.TextInput(attrs={'class':'form-control'}))
    your_message =  forms.CharField(label='Your Message', required=True,
                                widget=forms.Textarea(attrs={'class':'form-control'}))
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class':'form-control'}))

    system_subject = forms.CharField(required=True,
                              widget=forms.HiddenInput())
    leader = forms.ModelChoiceField(queryset=Leader.objects.filter(active=True),
                                    required=True,
                                    widget=forms.HiddenInput())
    def send_contact_email(self):
        name = self.cleaned_data.get('your_name', 'unknown')
        email = self.cleaned_data['your_email']
        message = self.cleaned_data['your_message']
        leader = self.cleaned_data['leader']
        system_subject = self.cleaned_data['system_subject']
        user_subject = self.cleaned_data['subject'] 
        
        subject = system_subject + ' - ' + user_subject
        leader_email = leader.email
        context = {'name':name, 'email': email,
                    'message':message}
        body = render_to_string('contact_email_template.html', context)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                 [leader_email], fail_silently=False)


class PrayerForm(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'form-control'}),
                                help_text="(Optional)")
    your_email = forms.EmailField(label='Your Email', max_length=100,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class':'form-control'}),
                                  help_text="(Optional)")
    prayer_request = forms.CharField(label='Prayer Request', required=True,
                                widget=forms.Textarea(attrs={'class':'form-control'}))
    prayer_meeting = forms.BooleanField(required=False,
                            label='Please pray for request during prayer meeting')
    follow_up = forms.BooleanField(required=False,
                        label='Please follow up with me')
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'class':'form-control'}))

    def send_prayer_email(self):
        name = self.cleaned_data.get('your_name', 'unknown')
        email = self.cleaned_data.get('your_email','unknown')
        prayer_request = self.cleaned_data['prayer_request']
        prayer_meeting = self.cleaned_data['prayer_meeting']
        follow_up = self.cleaned_data['follow_up']
        
        subject = "Living Hope Prayer request from %s" % name
        context = {'name':name, 'prayer_request': prayer_request,
                    'prayer_meeting':prayer_meeting, 'follow_up':follow_up}
        body = render_to_string('prayer_email_template.html', context)
        
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                 settings.EMAIL_RECIPIENTS, fail_silently=False)

def validate_parsable(value):
    if not test_parsable(value):
        raise ValidationError("Oops! We don't understand what you typed or the verses don't exist.")

class SearchVerseForm(forms.Form):
    query = forms.CharField(validators=[validate_parsable,])