from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionStatusSerializer
from users.permissions import IsModerator, IsModeratorReadOnly, IsOwner
from django.shortcuts import get_object_or_404


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated | IsModeratorReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.all()
        if user.is_authenticated:
            if user.groups.filter(name='Moderators').exists() or user.is_staff:
                queryset = queryset.order_by('name')  # Сортировка по имени курса
            else:
                queryset = queryset.filter(owner=user).order_by('name')  # Сортировка по имени курса
        else:
            queryset = Course.objects.none()
        return queryset


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user,)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]
    pagination_class = CustomPagination

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
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

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
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class SubscriptionAPIView(APIView):

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item, created = Subscription.objects.get_or_create(user=user, course=course_item)

        if created:
            message = 'подписка добавлена'
        else:
            subs_item.delete()
            message = 'подписка удалена'

        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        serializer = SubscriptionStatusSerializer(subscriptions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
