# tasks.py
from datetime import timedelta, datetime

import pytz
from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .models import User, Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Задача для отправки e-mail подписчикам курса"""

    course = Course.objects.get(id=course_id)
    subscribers = User.objects.filter(subscription__course=course)
    for user in subscribers:
        send_mail(
            subject='Обновление курса',
            message=f'Курс "{course.name}" был обновлен.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    """Задача для блокировки пользователей по полю last_login"""

    timezone = pytz.UTC
    one_month_ago = datetime.now(timezone) - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True, is_staff=False)
    inactive_users.update(is_active=False)
