from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson
from django.utils import timezone


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **kwargs):
        # Создаем пользователей
        user1 = User.objects.create(email='user1@example.com', password='password1', is_active=True)
        user2 = User.objects.create(email='user2@example.com', password='password2', is_active=True)
        user3 = User.objects.create(email='user3@example.com', password='password3', is_active=True)

        self.stdout.write(self.style.SUCCESS('Пользователи созданы'))

        # Создаем курсы
        course1 = Course.objects.create(owner=user1, name='Course 1', description='Description for Course 1')
        course2 = Course.objects.create(owner=user2, name='Course 2', description='Description for Course 2')

        self.stdout.write(self.style.SUCCESS('Курсы созданы'))

        # Создаем уроки для курсов
        lesson1 = Lesson.objects.create(owner=user1, name='Lesson 1', description='Description for Lesson 1',
                                         video_link='https://example.com/lesson1', course=course1)
        lesson2 = Lesson.objects.create(owner=user2, name='Lesson 2', description='Description for Lesson 2',
                                         video_link='https://example.com/lesson2', course=course2)

        self.stdout.write(self.style.SUCCESS('Уроки созданы'))

        # Создаем платежи
        Payment.objects.create(user=user1, payment_date=timezone.now(), course=course1, amount=100.00, payment_method='cash')
        Payment.objects.create(user=user2, payment_date=timezone.now(), lesson=lesson2, amount=50.00, payment_method='card')
        Payment.objects.create(user=user1, payment_date=timezone.now() - timezone.timedelta(days=2), course=course1, amount=10.00, payment_method='card')
        Payment.objects.create(user=user2, payment_date=timezone.now() - timezone.timedelta(days=2), course=course1, amount=180.00, payment_method='card')
        Payment.objects.create(user=user1, payment_date=timezone.now() - timezone.timedelta(days=2), course=course1, amount=840.00, payment_method='cash')

        self.stdout.write(self.style.SUCCESS('Платежи созданы'))