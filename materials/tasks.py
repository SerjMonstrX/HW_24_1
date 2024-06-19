# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from .models import User, Course, Subscription

@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = User.objects.filter(subscriptions__course=course)
    for user in subscribers:
        send_mail(
            'Course Update',
            f'Курс "{course.name}" был обновлен.',
            'admin@admin.com',
            [user.email],
            fail_silently=False,
        )