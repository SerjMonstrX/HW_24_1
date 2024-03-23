from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name')
    list_filter = ('owner',)
    search_fields = ('owner', 'name')


@admin.register(Lesson)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'course')
    list_filter = ('owner',)
    search_fields = ('owner', 'name', 'course')
