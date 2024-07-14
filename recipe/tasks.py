# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    logger.info("Sending email")
    print("Mail Task received")
    pass

@shared_task
def daily_notification_task():
    logger.info("Daily Notification Log")
    print("Daily Notification")
    # Your logic to send daily notifications
    pass
