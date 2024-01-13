from django import forms

from mailing.models import Mailing, Message


class MailingForms(forms.ModelForm):

    class Meta:
        model = Mailing
        #fields = '__all__'
        fields = ('mailing_time', 'periodicity', 'status', 'message')

class MessageForms(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('theme','body')


