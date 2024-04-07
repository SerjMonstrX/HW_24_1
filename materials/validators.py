import re
from rest_framework.exceptions import ValidationError


class VideoLinkValidator:
    """ Валидация URL-адреса видео """

    def __init__(self, field):
        self.field = field
        self.allowed_video_url = ['youtu.be', 'www.youtube.com', 'youtube.com']

    def __call__(self, value):
        # Получение значения поля
        tmp_val = dict(value).get(self.field)
        # Получаем пересечение множеств, содержащих строки
        set_url = set(tmp_val.split('/')) & set(self.allowed_video_url)
        if len(set_url) == 0:
            raise ValidationError('Ссылка на недопустимый ресурс!')
