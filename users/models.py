from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


NULLABLE = {'blank': True, 'null': True}
PAYMENT_METHOD_CHOICES = (
    ('cash', 'Наличные'),
    ('card', 'Карта'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        from materials.models import Course, Lesson  # Импорт здесь

        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    avatar = models.ImageField(upload_to='avatars', verbose_name='аватар', **NULLABLE)
    phone_number = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Payment(models.Model):
    from materials.models import Course, Lesson  # Импорт здесь
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='отдельно оплаченный урок', **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')
    session_id = models.CharField(max_length=255, verbose_name="ID сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='ссылка на оплату', **NULLABLE)

    def __str__(self):
        return f'{self.user} - оплачено {self.course}, {self.lesson}.'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
