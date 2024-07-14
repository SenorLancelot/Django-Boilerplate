# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_task(subject, message, from_email, recipient_list):

    print("Mail Task received")
    pass

@shared_task
def daily_notification_task():
    print("Daily Notification")
    # Your logic to send daily notifications
    pass
