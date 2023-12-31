from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, main, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('list/', MailingListView.as_view(), name='list'),
    path('view/<int:pk>', MailingDetailView.as_view(), name='view_mailing'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>', MessageUpdateView.as_view(),name='update_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(),name='delete_message'),
            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)