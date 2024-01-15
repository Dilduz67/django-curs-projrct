import pytz
from django.conf import settings
from django.core.cache import cache
import smtplib

from blog.models import Article
from client.models import Client

from datetime import datetime
from django.core.mail import send_mail

from mailing.models import Log, Mailing


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

def swnd_mails(mailings):
    for mailing in mailings:
        now = datetime.datetime.now()
        for ms in Mailing.objects.filter(status=2):
            ml = Log.objects.filter(mailing=ms)
            if ml.exists():
                last_try_date = ml.order_by('-date_attempt').first()
                if ms.period == 1:                                  #DAILY
                    if (now - last_try_date).days >= 1:
                        send_email(mailing)
                elif ms.period == 2:                                #WEEKLY
                    if (now - last_try_date).days >= 7:
                        send_email(mailing)
                elif ms.period == 3:                                #MONTHLY
                    if (now - last_try_date).days >= 30:
                        send_email(mailing)
            else:
                send_email(mailing)

def send_email(mailing):
    tz = pytz.timezone('Europe/Moscow')

    clients = [client.email for client in Client.objects.filter(user=mailing.user)]

    mail_subject = mailing.message.body if mailing.message is not None else 'Рассылка'
    message = mailing.massage.theme if mailing.message is not None else 'Вам назначена рассылка'
    try:
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
        log = Log.objects.create(date_attempt=datetime.now(tz), status='Успешно', answer='200')
        log.save()
    except smtplib.SMTPException as err:
        log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err)
        log.save()

