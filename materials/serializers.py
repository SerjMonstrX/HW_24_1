from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lessons.count()  # lessons из модели Courses через related_name


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course']


class SubscriptionStatusSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['user', 'course', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj.course).exists()
