# Generated by Django 4.2.11 on 2024-04-06 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0008_alter_course_preview_alter_lesson_preview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='preview',
        ),
    ]