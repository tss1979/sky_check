from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailings.models import Notification, Client


def get_cached_mailing_count():
    if CACHE_ENABLED:
        mailing_count = cache.get('mailing_count')
        if mailing_count is None:
            mailing_count = len(Notification.objects.all())
            cache.set('mailing_count', mailing_count)
    else:
        mailing_count = len(Notification.objects.all())
    return mailing_count

def get_cached_active_mailings():
    if CACHE_ENABLED:
        active_mailings = cache.get('active_mailings')
        if active_mailings is None:
            active_mailings = len(Notification.objects.filter(status='p'))
            cache.set('active_mailings', active_mailings)
    else:
        active_mailings = len(Notification.objects.filter(status='p'))
    return active_mailings

def get_cached_users_count():
    if CACHE_ENABLED:
        users_count = cache.get('users_count')
        if users_count is None:
            users_count = len(Client.objects.all().distinct())
            cache.set('users_count', users_count)
    else:
        users_count = len(Client.objects.all().distinct())
    return users_count



