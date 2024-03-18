from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson, NULLABLE


PAYMENT_METHOD_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Карта'),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватар', **NULLABLE)
    phone_number = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='отдельно оплаченный урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.user} - оплачено {self.course}, {self.lesson}.'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
