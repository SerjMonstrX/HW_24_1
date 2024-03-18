from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создание пользователей'

    def handle(self, *args, **kwargs):
        # Создаем пользователей
        User.objects.create(email='user1@example.com', password='password1')
        User.objects.create(email='user2@example.com', password='password2')
        User.objects.create(email='user3@example.com', password='password3')
        self.stdout.write(self.style.SUCCESS('Пользователи созданы'))