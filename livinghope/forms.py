from django import forms
from django.conf import settings
from captcha.fields import CaptchaField, CaptchaTextInput
from django.template.loader import render_to_string
from django.core.mail import send_mail
from livinghope.models import Leader
# from django.utils.safestring import mark_safe

# class BootstrapCaptchaField(CaptchaField):
#     def __init__(self, *args, **kwargs):
#         super(CaptchaField, self).__init__()

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
                 ['rhsiao2@gmail.com'], fail_silently=False)

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
                 ['rhsiao2@gmail.com'], fail_silently=False)
