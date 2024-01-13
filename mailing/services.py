import pytz
from django.conf import settings
from django.core.cache import cache
import smtplib

from blog.models import Article
from client.models import Client

from datetime import datetime
from django.core.mail import send_mail

from mailing.models import Log


def get_cache_version_for_article(article_pk):
    if settings.CACHE_ENABLED:
        key = f'article_list{article_pk}'
        article_list = cache.get(key)
        if article_list is None:
            article_list = Article.objects.filter(article__pk=article_pk)
            cache.set(key, article_list)
    else:
        article_list = Article.objects.filter(article__pk=article_pk)
    return article_list

def swnd_mail(mailings):
    tz = pytz.timezone('Europe/Moscow')

    for new_mailing in mailings:
        clients = [client.email for client in Client.objects.filter(user=new_mailing.user)]
        if new_mailing.mailing_time >= datetime.now(tz):
            mail_subject = new_mailing.message.body if new_mailing.message is not None else 'Рассылка'
            message = new_mailing.massage.theme if new_mailing.message is not None else 'Вам назначена рассылка'
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Успешно', answer='200')
                log.save()
            except smtplib.SMTPException as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err)
                log.save()
                # raise err
            new_mailing.status = 3
            new_mailing.save()

