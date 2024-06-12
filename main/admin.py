"""
This module configures the admin interface for the Django application.

It registers the Course, Student, CourseToStudent, and Review models with the admin site,
and defines how these models should be displayed in the admin interface.
"""

from django.contrib import admin

from .models import Course, CourseToStudent, Review, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for the Course model."""

    list_display = ('title', 'description')
    readonly_fields = ('id',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for the Student model."""

    list_display = ('first_name', 'last_name', 'date_of_receipt', 'user')
    readonly_fields = ('id',)


@admin.register(CourseToStudent)
class CourseToStudentAdmin(admin.ModelAdmin):
    """Admin interface for the CourseToStudent model."""

    list_display = ('course', 'student')
    readonly_fields = ('id',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for the Review model."""

    list_display = ('course', 'student', 'review_text', 'grade')
    readonly_fields = ('id',)
