"""
This module defines the models for the Django application.

It includes models for Course, Student, CourseToStudent, and Review.
"""

from datetime import date
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

MAX_LENGTH = 30
MAX_LENGTH_DESCRIPTION = 1000


def validate_future_date(date_value):
    """
    Validate that the given date is not in the past.

    Args:
        date_value (date): The date to validate.

    Raises:
        ValidationError: If the date is in the past.
    """
    if date_value > date.today():
        raise ValidationError('Date cannot be in the past.', params={'value': date_value})


class MinMaxIntegerField(models.IntegerField):
    """An IntegerField that restricts its values to be between 1 and 5."""

    def formfield(self, **kwargs):
        """
        Return a form field with min and max values set.

        This method overrides the base formfield method to set the min_value and max_value
        attributes of the form field to 1 and 5 respectively.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the base formfield method.

        Returns:
            formfield: A form field with min and max values set.
        """
        return super().formfield(min_value=1, max_value=5, **kwargs)


class UserMixin(models.Model):
    """Abstract model that includes a foreign key to the User model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Abstract model that includes a UUID primary key field."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Course(UUIDMixin, UserMixin):
    """Model representing a course."""

    title = models.TextField(MAX_LENGTH)
    description = models.TextField(MAX_LENGTH_DESCRIPTION)

    students = models.ManyToManyField('Student', through='CourseToStudent')

    def __str__(self) -> str:
        """
        Return the title of the course.

        Returns:
            str: The title of the course.
        """
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['title']


class Student(UUIDMixin, UserMixin):
    """Model representing a student."""

    first_name = models.TextField(MAX_LENGTH)
    last_name = models.TextField(MAX_LENGTH)
    date_of_receipt = models.DateField(validators=[validate_future_date])

    courses = models.ManyToManyField('Course', through='CourseToStudent')

    def __str__(self) -> str:
        """
        Return the first name of the student.

        Returns:
            str: The first name of the student.
        """
        return self.first_name

    class Meta:
        verbose_name = 'Studen'
        verbose_name_plural = 'Students'
        ordering = ['last_name']


class CourseToStudent(UUIDMixin):
    """Model representing the relationship between a course and a student."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Return a string representing the relationship between a course and a student.

        Returns:
            str: A string in the format 'course to student'.
        """
        return f'{self.course} to {self.student}'

    class Meta:
        verbose_name = 'CourseToStudent'
        verbose_name_plural = 'CoursesToStudents'
        unique_together = ('course', 'student')
        ordering = ['course']


class Review(UUIDMixin):
    """Model representing a review of a course by a student."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='review')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='review')
    review_text = models.TextField(null=True, blank=True, max_length=100)
    grade = MinMaxIntegerField(default=5)

    def __str__(self) -> str:
        """
        Return a string representing the review of a course by a student.

        Returns:
            str: A string in the format 'Review for course title by student first name'.
        """
        return f'Review for {self.course.title} by {self.student.first_name}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['grade']
