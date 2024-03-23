from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец курса', related_name='courses')
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='courses/previews', verbose_name='логотип',  **NULLABLE)
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
    preview = models.ImageField(upload_to='lessons/previews', verbose_name='логотип',  **NULLABLE)
    video_link = models.URLField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='принадлежность к курсу', related_name='lessons')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
