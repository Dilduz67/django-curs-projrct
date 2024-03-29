from datetime import datetime

import smtplib
import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail

from blog.models import Article
from client.models import Client
from mailing.forms import MailingForms, MessageForms
from mailing.models import Mailing, Log, Message


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    #queryset = Mailing.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'log_list_{self.object.pk}'
            log_list = cache.get(key)
            if log_list is None:
                log_list = self.object.log_set.all()
                cache.set(key, log_list)
        else:
            log_list = self.object.log_set.all()
        context_data['logs'] = log_list

        return context_data



def main(request):
    clients = len(Client.objects.all().distinct('email'))
    article = Article.objects.filter(is_published=True).order_by('?')
    mailing = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(status=2))
    context = {
        'title': "Главная",
        'article': article[:3],
        'mailing': mailing,
        'mailing_active': mailing_active,
        'clients': clients
    }
    return render(request, 'mailing/main.html', context)


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForms
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.add_mailing'

    def form_valid(self, form):
        #tz = pytz.timezone('Europe/Moscow')
        #clients = [client.email for client in Client.objects.filter(user=self.request.user)]
        form.instance.status = 2
        form.instance.user = self.request.user
        form.save()
        #new_mailing = form.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForms
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.change_mailing'



class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')
    permission_required = 'mailing.delete_mailing'


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    queryset = Message.objects.all()

    #def get_queryset(self):
    #    return super().get_queryset().filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForms
    template_name = 'mailing/create_message.html'
    success_url = reverse_lazy('mailing:message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForms
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        return super().form_valid(form)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')



