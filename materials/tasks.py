# tasks.py
from datetime import timezone, timedelta

from celery import shared_task, Celery
from celery.schedules import crontab
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .models import User, Course, Subscription


@shared_task
def send_course_update_email(course_id):
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
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)


app = Celery('config')

app.conf.beat_schedule = {
    'deactivate-inactive-users-every-day': {
        'task': 'users.tasks.deactivate_inactive_users',
        'schedule': crontab(hour=0, minute=0),
    },
}

app.conf.timezone = 'UTC'
