
from django.conf import settings
from mailing.models import Mailing, Log
from services import send_mail


def my_scheduled_job():
    mailings = Mailing.objects.all()
    send_mail(mailings)




