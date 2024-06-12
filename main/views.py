"""
This module contains views for the application.

It includes views for user register, login, and logout, as well as views for managing courses, students, and reviews.
"""

from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .forms import ReviewForm
from .models import Course, CourseToStudent, Review, Student
from .serializers import (CourseSerializer, CourseToStudentSerializer,
                          ReviewSerializer, StudentSerializer)


class UserAdminPermission(permissions.BasePermission):
    """
    Custom permission class that allows access to safe methods for any user.

    And gives full access to staff users or the user who owns the object.

    Attributes:
        _safe_methods (list): List of HTTP methods considered safe.
    """

    _safe_methods = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the request.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view the request was made to.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, target_object):
        """
        Check if the user has permission to perform the request on the target_object.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view the request was made to.
            target_object (Model): The object the request is for.

        Returns:
            bool: True if the user is staff or owns the target_object, or if the request method is safe.
        """
        if request.method in self._safe_methods:
            return True
        return request.user.is_staff or target_object.user == request.user


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Course instances.

    Attributes:
        queryset (QuerySet): The set of all Course instances.
        serializer_class (Serializer): The serializer class for Course instances.
        permission_classes (list): List of permission classes applied to this ViewSet.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [UserAdminPermission]

    def perform_create(self, serializer):
        """
        Save the instance created by the serializer with the user from the request.

        Args:
            serializer (Serializer): The serializer for Course instances.
        """
        serializer.save(user=self.request.user)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Student instances.

    Attributes:
        queryset (QuerySet): The set of all Student instances.
        serializer_class (Serializer): The serializer class for Student instances.
        permission_classes (list): List of permission classes applied to this ViewSet.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [UserAdminPermission]

    def perform_create(self, serializer):
        """
        Save the instance created by the serializer with the user from the request.

        Args:
            serializer (Serializer): The serializer for Student instances.
        """
        serializer.save(user=self.request.user)


class CourseToStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing CourseToStudent instances.

    Attributes:
        queryset (QuerySet): The set of all CourseToStudent instances.
        serializer_class (Serializer): The serializer class for CourseToStudent instances.
        permission_classes (list): List of permission classes applied to this ViewSet.
    """

    queryset = CourseToStudent.objects.all()
    serializer_class = CourseToStudentSerializer
    permission_classes = [UserAdminPermission]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Review instances.

    Attributes:
        queryset (QuerySet): The set of all Review instances.
        serializer_class (Serializer): The serializer class for Review instances.
        permission_classes (list): List of permission classes applied to this ViewSet.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [UserAdminPermission]

    def perform_create(self, serializer):
        """
        Save the instance created by the serializer with the student from the request.

        Args:
            serializer (Serializer): The serializer for Review instances.
        """
        student = Student.objects.get(user=self.request.user)
        serializer.save(student=student)


class UserRegistrationView(APIView):
    """
    View for user registration.

    Attributes:
        permission_classes (list): List of permission classes applied to this View.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle POST request to register a new user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object.
        """
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not password1 or not password2:
            return render(request, 'register.html', {'error': 'Имя пользователя и пароль обязательны для заполнения!'})
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Пароли не совпадают!'})
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create_user(username=username, password=password1)
        else:
            return render(request, 'register.html', {'error': 'Пользователь с таким именем уже существует!'})
        login(request=request, user=user)
        return redirect('main')

    def get(self, request):
        """
        Handle GET request to show the registration form.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object.
        """
        return render(request, 'register.html')


class UserLoginView(APIView):
    """
    View for user login.

    Attributes:
        permission_classes (list): List of permission classes applied to this View.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle POST request to log in a user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return render(request, 'login.html', {'error': 'Имя пользователя и пароль обязательны для заполнения!'})
        user = User.objects.filter(username=username).first()
        if user is None:
            return render(request, 'login.html', {'error': 'Пользователь не найден!'})
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'error': 'Введен неверный пароль!'})
            token, _ = Token.objects.get_or_create(user=user)
        login(request=request, user=user)
        return redirect('main')

    def get(self, request):
        """
        Handle GET request to show the login form.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object.
        """
        return render(request, 'login.html')


def log_out(request):
    """
    Log out the current user.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('main')


def main(request):
    """
    Render the main page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, 'main.html')


def student(request, student_id):
    """
    Render the student page.

    Args:
        request (HttpRequest): The request object.
        student_id (uuid): The ID of the student.

    Returns:
        HttpResponse: The response object.
    """
    student_obj = Student.objects.get(id=student_id)
    return render(request, 'student.html', {'student': student_obj, 'request': request})


def check_student_in_course(student_obj, course_obj):
    """
    Check if a student is in a course.

    Args:
        student_obj (Student): The student object.
        course_obj (Course): The course object.

    Returns:
        bool: True if the student is in the course, False otherwise.
    """
    return CourseToStudent.objects.filter(student=student_obj, course=course_obj).exists()


@login_required(login_url='login')
def course(request, course_id):
    """
    Render the course page.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = Course.objects.get(id=course_id)
    try:
        student_obj = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect('create_student')
    context = {
        'course': course_obj,
        'sitc': check_student_in_course(student_obj, course_obj),
    }
    return render(request, 'course.html', context)


def review(request, review_id):
    """
    Render the review page.

    Args:
        request (HttpRequest): The request object.
        review_id (uuid): The ID of the review.

    Returns:
        HttpResponse: The response object.
    """
    review_obj = Review.objects.get(id=review_id)
    return render(request, 'review.html', {'review': review_obj})


def coursetostudent(request, coursetostudent_id):
    """
    Render the coursetostudent page.

    Args:
        request (HttpRequest): The request object.
        coursetostudent_id (uuid): The ID of the coursetostudent.

    Returns:
        HttpResponse: The response object.
    """
    coursetostudent_obj = CourseToStudent.objects.get(id=coursetostudent_id)
    return render(request, 'coursetostudent.html', {'coursetostudent': coursetostudent_obj})


def students(request):
    """
    Render the students page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    students_obj = Student.objects.all()
    return render(request, 'students.html', {'students': students_obj})


def courses(request):
    """
    Render the courses page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    courses_obj = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses_obj})


def reviews(request):
    """
    Render the reviews page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    reviews_obj = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews_obj})


def coursetostudents(request):
    """
    Render the coursetostudents page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    coursestostudents_obj = CourseToStudent.objects.all()
    return render(request, 'coursestostudents.html', {'coursestostudents': coursestostudents_obj})


@login_required(login_url='login')
def create_student(request):
    """
    Create a new student.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        if Student.objects.filter(user=request.user).exists():
            return render(request, 'create_student.html', {'error': 'Вы уже создали студента!'})
        student_obj = Student()
        student_obj.first_name = request.POST.get('first_name')
        student_obj.last_name = request.POST.get('last_name')
        date_of_receipt_str = request.POST.get('date_of_receipt')
        date_of_receipt = datetime.strptime(date_of_receipt_str, '%Y-%m-%d').date()
        if date_of_receipt > date.today():
            return render(request, 'create_student.html', {'error': 'Дата поступления не может быть в будущем!'})
        student_obj.date_of_receipt = date_of_receipt
        student_obj.user = request.user
        student_obj.save()
        return redirect('students')
    return render(request, 'create_student.html')


def edit_student(request, student_id):
    """
    Edit an existing student.

    Args:
        request (HttpRequest): The request object.
        student_id (uuid): The ID of the student.

    Returns:
        HttpResponse: The response object.
    """
    student_obj = Student.objects.get(id=student_id)
    if request.method == 'POST':
        if request.user == student_obj.user or request.user.is_staff:
            student_obj.first_name = request.POST.get('first_name')
            student_obj.last_name = request.POST.get('last_name')
            date_of_receipt_str = request.POST.get('date_of_receipt')
            date_of_receipt = datetime.strptime(date_of_receipt_str, '%Y-%m-%d').date()
            if date_of_receipt > date.today():
                context = {
                    'error': 'Дата поступления не может быть в будущем!',
                    'student': student_obj,
                }
                return render(request, 'edit_student.html', context)
            student_obj.date_of_receipt = date_of_receipt
            student_obj.save()
            return redirect('students')
        return render(request, 'edit_student.html', {'error': 'Вы можете редактировать только своего студента!'})

    if request.user == student_obj.user or request.user.is_staff:
        return render(request, 'edit_student.html', {'student': student_obj})
    return render(request, 'edit_student.html', {'error': 'Вы можете редактировать только своего студента!'})


def delete_student(request, student_id):
    """
    Delete an existing student.

    Args:
        request (HttpRequest): The request object.
        student_id (uuid): The ID of the student.

    Returns:
        HttpResponse: The response object.
    """
    student_obj = Student.objects.get(id=student_id)
    if request.user == student_obj.user or request.user.is_staff:
        student_obj.delete()
        return redirect('students')
    return render(request, 'delete_student.html', {'error': 'Вы можете удалять только своего студента!'})


@login_required(login_url='login')
def create_course(request):
    """
    Create a new course.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user = request.user
        new_course = Course(title=title, description=description, user=user)
        new_course.save()
        return redirect('courses')
    return render(request, 'create_course.html')


def edit_course(request, course_id):
    """
    Edit an existing course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = Course.objects.get(id=course_id)
    if request.method == 'POST':
        if request.user == course_obj.user or request.user.is_staff:
            course_obj.title = request.POST.get('title')
            course_obj.description = request.POST.get('description')
            course_obj.save()
            return redirect('courses')
        return render(request, 'edit_course.html', {'error': 'Вы можете редактировать только свой курс!'})
    return render(request, 'edit_course.html', {'course': course_obj})


def delete_course(request, course_id):
    """
    Delete an existing course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = Course.objects.get(id=course_id)
    if request.user == course_obj.user or request.user.is_staff:
        course_obj.delete()
        return redirect('courses')
    return render(request, 'delete_course.html', {'error': 'Вы можете удалять только свой курс!'})


def create_review(request, course_id):
    """
    Create a new review for a course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    course_obj = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated and request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review_obj = form.save(commit=False)
            review_obj.course_id = course_obj.id
            student_obj = Student.objects.get(user=request.user)
            review_obj.student = student_obj
            review_obj.save()
            return redirect('main')
        messages.error(request, 'Ошибка валидации')
    else:
        form = ReviewForm(user=request.user)
    students_obj = Student.objects.filter(user=request.user) if request.user.is_authenticated else None
    courses_obj = Course.objects.all()
    context = {
        'form': form,
        'course': course_obj,
        'students': students_obj,
        'courses': courses_obj,
    }
    return render(request, 'create_review.html', context)


def edit_review(request, review_id):
    """
    Edit an existing review.

    Args:
        request (HttpRequest): The request object.
        review_id (uuid): The ID of the review.

    Returns:
        HttpResponse: The response object.
    """
    review_obj = Review.objects.get(id=review_id)
    if request.method == 'POST':
        if request.user == review_obj.student.user or request.user.is_staff:
            form = ReviewForm(request.POST, user=request.user, instance=review_obj)
            if form.is_valid():
                form.save()
                return redirect('courses')
        else:
            return render(request, 'edit_review.html', {'error': 'Вы можете редактировать только свой отзыв!'})
    else:
        form = ReviewForm(user=request.user, instance=review_obj)
    return render(request, 'edit_review.html', {'form': form, 'review': review_obj})


def delete_review(request, review_id):
    """
    Delete an existing review.

    Args:
        request (HttpRequest): The request object.
        review_id (uuid): The ID of the review.

    Returns:
        HttpResponse: The response object.
    """
    review_obj = get_object_or_404(Review, id=review_id)
    if request.user == review_obj.student.user or request.user.is_staff:
        review_obj.delete()
        return redirect('courses')
    return render(request, 'reviews.html', {'error': 'Вы можете удалять только свои отзывы!'})


def course_students(request, course_id):
    """
    Display all students for a specific course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = get_object_or_404(Course, id=course_id)
    students_obj = course_obj.students.all()
    return render(request, 'course_students.html', {'course': course_obj, 'students': students_obj})


def student_courses(request, student_id):
    """
    Display all courses for a specific student.

    Args:
        request (HttpRequest): The request object.
        student_id (uuid): The ID of the student.

    Returns:
        HttpResponse: The response object.
    """
    students_obj = get_object_or_404(Student, id=student_id)
    course_obj = students_obj.courses.all()
    return render(request, 'student_courses.html', {'student': students_obj, 'courses': course_obj})


def course_reviews(request, course_id):
    """
    Display all reviews for a specific course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = get_object_or_404(Course, id=course_id)
    reviews_obj = Review.objects.filter(course=course_obj)
    return render(request, 'course_reviews.html', {'course': course_obj, 'reviews': reviews_obj})


@login_required
def enroll_course(request, course_id):
    """
    Enroll a student in a course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = Course.objects.get(id=course_id)
    try:
        student_obj = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'create_student.html', {
            'error': 'Вы должны быть зарегистрированы как студент, чтобы поступить на курс',
        })

    if CourseToStudent.objects.filter(student=student_obj, course=course_obj).exists():
        return render(request, 'courses.html', {
            'error': 'Вы уже поступили на этот курс',
        })

    CourseToStudent.objects.create(student=student_obj, course=course_obj)
    return redirect('courses')


def unenroll_course(request, course_id):
    """
    Unenroll a student from a course.

    Args:
        request (HttpRequest): The request object.
        course_id (uuid): The ID of the course.

    Returns:
        HttpResponse: The response object.
    """
    course_obj = Course.objects.get(id=course_id)
    student_obj = Student.objects.get(user=request.user)
    try:
        course_to_student = CourseToStudent.objects.get(student=student_obj, course=course_obj)
    except CourseToStudent.DoesNotExist:
        context = {
            'error': 'Вы уже покинули этот курс',
            'student_in_this_course': CourseToStudent.objects.filter(student=student_obj, course=course_obj).exists(),
            'course': course_obj,
            'student': student_obj,
        }
        return render(request, 'courses.html', context)

    course_to_student.delete()
    return redirect('courses')
