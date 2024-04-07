import os

from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(email='user_1@test.ru')

        # Создание курса
        self.course_1 = Course.objects.create(
            name="course_test_1",
            description="Course_desc_test_1",
            owner=self.user_1
        )

        # Проверка создания курса
        self.assertIsNotNone(self.course_1, "Failed to create course in setUp()")

        # Создание урока
        self.lesson_1 = Lesson.objects.create(
            name="name_lesson_1",
            description="description_lesson_1",
            video_link="https://www.youtube.com/watch?v=w1ucZCmvO5c",
            preview=os.path.join('materials', 'previews', 'lessons', 'logo.png'),
            course=self.course_1,
            owner=self.user_1
        )

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user_1)

    def test_create_lesson(self):
        """Тестирование создание урока"""
        data = model_to_dict(self.lesson_1)

        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем содержимое созданной записи
        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'name': 'name_lesson_1',
                'description': 'description_lesson_1',
                'preview': response.json()['preview'],
                'video_link': 'https://www.youtube.com/watch?v=w1ucZCmvO5c',
                'owner': self.user_1.pk,
                'course': response.json()['course'],
            }
        )

        # Проверяем наличие записи в базе данных
        self.assertTrue(Lesson.objects.filter(id=response.json()['id']).exists())

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        data = {
            "course_id": self.course_1.id
        }
        response = self.client.post(
            '/subscription/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_lesson(self):
        """ Тестирование вывода списка """

        response = self.client.get(
            '/lesson/'
        )

        # Проверяем вывод списка записей
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response.json(),
            {
                'count': response.json()['count'],
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': response.json()['results'][0]['id'],
                        'name': 'name_lesson_1',
                        'description': 'description_lesson_1',
                        'preview': response.json()['results'][0]['preview'],
                        'video_link': 'https://www.youtube.com/watch?v=w1ucZCmvO5c',
                        'owner': self.user_1.pk,
                        'course': response.json()['results'][0]['course'],
                    }
                ]
            }
        )

    def test_detail_lesson(self):
        """ Тестирование вывода урока """

        data = model_to_dict(self.lesson_1)

        response_create = self.client.post(
            '/lesson/create/',
            data=data
        )

        response_detail = self.client.get(
            f"/lesson/{response_create.json()['id']}/"
        )

        # Проверяем вывод одной записи
        self.assertEqual(
            response_detail.status_code,
            status.HTTP_200_OK
        )

        # Проверяем содержимое выводимой записи
        self.assertEqual(
            response_detail.json(),
            {
                'id': response_detail.json()['id'],
                'name': 'name_lesson_1',
                'description': 'description_lesson_1',
                'preview': response_detail.json()['preview'],
                'video_link': 'https://www.youtube.com/watch?v=w1ucZCmvO5c',
                'owner': self.user_1.pk,
                'course': response_detail.json()['course'],
            }
        )

    def test_update_lesson(self):
        """ Тестирование редактирования урока """

        response_create = self.client.post(
            '/lesson/create/',
            data=model_to_dict(self.lesson_1)
        )

        response_patch = self.client.patch(
            f"/lesson/update/{response_create.json()['id']}/",
            {
                'name': 'name_lesson_1_patch',
                'description': 'description_lesson_1_patch',
                'video_link': 'https://www.youtube.com/watch?v=w1ucZCmvO5c_patch',
            }
        )

        # Проверяем вывод одной записи
        self.assertEqual(
            response_patch.status_code,
            status.HTTP_200_OK
        )

        # Проверяем содержимое редактированной записи
        self.assertEqual(
            response_patch.json(),
            {
                'id': response_patch.json()['id'],
                'name': 'name_lesson_1_patch',
                'description': 'description_lesson_1_patch',
                'preview': response_patch.json()['preview'],
                'video_link': 'https://www.youtube.com/watch?v=w1ucZCmvO5c_patch',
                'owner': self.user_1.pk,
                'course': response_patch.json()['course'],
            }
        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока """

        response_create = self.client.post(
            '/lesson/create/',
            data=model_to_dict(self.lesson_1)
        )

        response_delete = self.client.delete(
            f"/lesson/delete/{response_create.json()['id']}/"
        )

        # Проверяем удаление
        self.assertEqual(
            response_delete.status_code,
            status.HTTP_204_NO_CONTENT
        )
