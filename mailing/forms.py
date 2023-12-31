from django import forms

from mailing.models import Mailing, Message


class MailingForms(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = '__all__'


class MessageForms(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


