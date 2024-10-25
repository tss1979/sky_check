# runapscheduler.py
import logging
import datetime
import smtplib

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.mail import send_mail
from mailings.models import Notification, NotificationAttempt

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_new_notification, 'interval', seconds=60)
    scheduler.start()

def send_mail_notification(mailings, current_datetime, attempts=None):
    for mailing in mailings:
        try:
            server_response =  send_mail(
                                    subject=mailing.message.title,
                                    message=mailing.message.body,
                                    from_email=settings.EMAIL_HOST_USER,
                                    recipient_list=[client.email for client in mailing.client.all()]
                                )
            if not mailing.first_send_time:
                mailing.first_send_time = current_datetime
            if mailing.status == 'c':
                mailing.status = 'p'
            mailing.last_send_time = current_datetime
            mailing.save()
            if attempts is not None:
                attempt = attempts.filter(notification=mailing)
                attempt.delete()
            NotificationAttempt.objects.create(last_attempt_at=current_datetime, is_sent=True,\
                                               server_message=server_response, notification=mailing)
        except smtplib.SMTPException as e:
            NotificationAttempt.objects.create(last_attempt_at=current_datetime, is_sent=False,\
                                               server_message=e, notification=mailing)


def send_new_notification():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.datetime.now(zone)

    mailings = list(Notification.objects.filter(start_at__lte=current_datetime,\
                                                finish_at__gte=current_datetime)\
                                         .filter(status='c'))

    processed_day = Notification.objects.filter(period='d', status='p')
    mailings.extend([mailing for mailing in processed_day if (current_datetime - mailing.last_send_time).days >= 1])
    processed_week = Notification.objects.filter(period='w', status='p')
    mailings.extend([mailing for mailing in processed_week if (current_datetime - mailing.last_send_time).days >= 7])
    processed_month = Notification.objects.filter(period='m', status='p')
    mailings.extend([mailing for mailing in processed_month if (current_datetime - mailing.last_send_time).days >= 30])

    send_mail_notification(mailings, current_datetime)

    failed = NotificationAttempt.objects.filter(is_sent=False)
    mailings_f = [attempt.notification for attempt in failed]
    send_mail_notification(mailings_f, current_datetime, failed)




# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_new_notification,
            trigger=CronTrigger(minute="*/1"),  # Every 1 week
            id="send_new_notification",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'send_new_notification'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")