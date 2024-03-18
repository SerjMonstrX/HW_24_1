from django.core.management.base import BaseCommand
from users.models import Payment
from django.utils import timezone


class Command(BaseCommand):
    help = 'Заполнение таблицы payment'

    def handle(self, *args, **kwargs):
        Payment.objects.create(
            user_id=1,
            payment_date=timezone.now(),
            course_id=1,
            amount=100.00,
            payment_method='cash'
        )
        Payment.objects.create(
            user_id=2,
            payment_date=timezone.now(),
            lesson_id=2,
            amount=50.00,
            payment_method='card'
        )
        Payment.objects.create(
            user_id=1,
            payment_date=timezone.now() - timezone.timedelta(days=2),
            course_id=1,
            amount=10.00,
            payment_method='card'
        )
        Payment.objects.create(
            user_id=2,
            payment_date=timezone.now() - timezone.timedelta(days=2),
            course_id=1,
            amount=180.00,
            payment_method='card'
        )
        Payment.objects.create(
            user_id=1,
            payment_date=timezone.now() - timezone.timedelta(days=2),
            course_id=1,
            amount=840.00,
            payment_method='cash'
        )
        self.stdout.write(self.style.SUCCESS('Таблица payment успешно заполнена'))
