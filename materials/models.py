from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец курса', related_name='courses')
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='previews/courses/', verbose_name='логотип', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец урока', related_name='lessons')
    name = models.CharField(max_length=100, verbose_name='название курса')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='previews/lessons/', verbose_name='логотип', **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='принадлежность к курсу', related_name='lessons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='название курса')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        unique_together = ('user', 'course')
