"""
This module defines the serializers for the Django REST framework application.

Serializers allow complex data such as querysets and model instances to be converted to
native Python datatypes that can then be easily rendered into JSON, XML or other content types.
"""

from rest_framework import serializers

from .models import Course, CourseToStudent, Review, Student


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for the Student model."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Student
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'


class CourseToStudentSerializer(serializers.ModelSerializer):
    """Serializer for the CourseToStudent model."""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CourseToStudent
        fields = '__all__'
