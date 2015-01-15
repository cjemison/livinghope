from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.template.loader import render_to_string
from django.core.mail import send_mail
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
        send_mail(subject, body, email,
                 ['rhsiao2@gmail.com'], fail_silently=False)

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
        email = self.cleaned_data.get('your_email','prayer@onelivinghope.com')
        prayer_request = self.cleaned_data['prayer_request']
        prayer_meeting = self.cleaned_data['prayer_meeting']
        follow_up = self.cleaned_data['follow_up']
        
        subject = "Living Hope Prayer request from %s" % name
        context = {'name':name, 'prayer_request': prayer_request,
                    'prayer_meeting':prayer_meeting, 'follow_up':follow_up}
        body = render_to_string('prayer_email_template.html', context)
        send_mail(subject, body, email,
                 ['rhsiao2@gmail.com'], fail_silently=False)
