from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsModeratorReadOnly


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated | IsModeratorReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists():
                return Course.objects.all()
            else:
                return Course.objects.filter(owner=user)
        return Course.objects.none()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return []
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course = Course.objects.get(pk=course_id)
        if course.owner == user:
            serializer.save(owner=user, course=course)
        else:
            # Если пользователь не владелец курса, не допускать создание урока
            raise PermissionDenied("У вас нет разрешения создавать уроки для чужого курса.")


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists():
                return Lesson.objects.all()
            else:
                return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerator]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return []
        else:
            lesson = self.get_object()  # Получаем объект урока
            if lesson.owner == self.request.user:  # Проверяем, является ли пользователь владельцем урока
                return [IsAuthenticated()]  # Разрешаем доступ, если пользователь является владельцем
            else:
                return []  # Запрещаем доступ, если пользователь не является владельцем и не модератор


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerator]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return []
        else:
            return [IsAuthenticated()]

    def perform_update(self, serializer):
        user = self.request.user
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(pk=lesson_id)
        if lesson.owner == user or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            # Если пользователь не владелец урока и не модератор, не допускать редактирование
            raise PermissionDenied("У вас нет разрешения редактировать этот урок.")

class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return []
        else:
            lesson = self.get_object()  # Получаем объект урока
            if lesson.owner == self.request.user:  # Проверяем, является ли пользователь владельцем урока
                return [IsAuthenticated()]  # Разрешаем доступ, если пользователь является владельцем
            else:
                return []  # Запрещаем доступ, если пользователь не является владельцем и не модератор