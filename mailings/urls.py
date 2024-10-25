from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import NotificationListView, NotificationDetailView, NotificationCreateView, \
    NotificationDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageDeleteView, ClientListView, \
    ClientDeleteView, ClientUpdateView, ClientCreateView, ClientDetailView, MessageUpdateView, NotificationUpdateView, \
    finish_notification, IndexView, AttemptListView

app_name = MailingsConfig.name



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('notifications', NotificationListView.as_view(), name='notifications'),
    path('notification/<int:pk>', NotificationDetailView.as_view(), name='notification_detail'),
    path('notification/create', NotificationCreateView.as_view(), name='notification_create'),
    path('notification/delete/<int:pk>', NotificationDeleteView.as_view(), name='notification_delete'),
    path('notification/update/<int:pk>', NotificationUpdateView.as_view(), name='notification_update'),
    path('notification/finish/<int:pk>', finish_notification, name='notification_finish'),
    path('messages', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('clients', ClientListView.as_view(), name='clients'),
    path('client/create', ClientCreateView.as_view(), name='client_create'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('notification-attempt', AttemptListView.as_view(), name='attempts'),
]