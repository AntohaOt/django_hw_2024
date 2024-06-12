"""
This module defines the URL routes for this Django application.

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.urls import path

from . import views
from .views import UserLoginView, UserRegistrationView, log_out

urlpatterns = [
    path('', views.main, name='main'),
    path('student/<uuid:student_id>/', views.student, name='student'),
    path('course/<uuid:course_id>/', views.course, name='course'),
    path('review/<uuid:review_id>/', views.review, name='review'),
    path('coursetostudent/<uuid:coursetostudent_id>/', views.coursetostudent, name='coursetostudent'),

    path('students/', views.students, name='students'),
    path('courses/', views.courses, name='courses'),
    path('reviews/', views.reviews, name='reviews'),
    path('coursestostudents/', views.coursetostudents, name='coursestostudents'),

    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),

    path('create_student/', views.create_student, name='create_student'),
    path('edit_student/<uuid:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<uuid:student_id>/', views.delete_student, name='delete_student'),

    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<uuid:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<uuid:course_id>/', views.delete_course, name='delete_course'),

    path('course/<uuid:course_id>/students/', views.course_students, name='course_students'),
    path('student/<uuid:student_id>/courses/', views.student_courses, name='student_courses'),
    path('course/<uuid:course_id>/reviews/', views.course_reviews, name='course_reviews'),

    path('create_review/<uuid:course_id>/', views.create_review, name='create_review'),
    path('edit_review/<uuid:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<uuid:review_id>/', views.delete_review, name='delete_review'),

    path('enroll_course/<uuid:course_id>/', views.enroll_course, name='enroll_course'),
    path('unenroll_course/<uuid:course_id>/', views.unenroll_course, name='unenroll_course'),
]
