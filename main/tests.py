"""
This module contains test cases for the Course, Student, and Review models.

It includes tests for the list, create, update, and delete endpoints of these models.
"""

import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from main.models import Course, CourseToStudent, Review, Student

from .forms import ReviewForm

HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_FOUND = 302


class TestCourse(TestCase):
    """Test case for the Course model."""

    _user_creds = {'username': 'abc', 'password': '123'}

    def setUp(self):
        """Set up the test environment for each test in this test case."""
        self.client = APIClient()
        self.user = User.objects.create(**self._user_creds)
        self.tocken = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.tocken)

    def test_course_list(self):
        """Test the course list endpoint."""
        response = self.client.get('/api/v1/courses/')
        self.assertEqual(response.status_code, HTTP_STATUS_OK)

    def test_course_create(self):
        """Test the course creation endpoint."""
        response = self.client.post('/api/v1/courses/', {'title': 'Course10', 'description': 'course10'})
        self.assertEqual(response.status_code, HTTP_STATUS_CREATED)
        self.assertIn('id', response.data)
        self.assertIn(response.data['id'], [str(course.id) for course in Course.objects.all()])

    def test_course_update(self):
        """Test the course update endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        course = Course.objects.create(title='Course10', description='course10', user=superuser).id

        response = self.client.put(f'/api/v1/courses/{course}/', {'title': 'Course10', 'description': 'course10'})
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertIn('id', response.data)
        self.assertEqual(Course.objects.get(title='Course10').description, 'course10')

    def test_course_delete(self):
        """Test the course delete endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        course = Course.objects.create(title='Course10', description='course1', user=superuser).id

        response = self.client.delete(f'/api/v1/courses/{course}/')
        self.assertEqual(response.status_code, HTTP_STATUS_NO_CONTENT)


class TestStudent(TestCase):
    """Test case for the Student model."""

    _user_creds = {'username': 'abc', 'password': '123'}

    def setUp(self):
        """Set up the test environment for each test in this test case."""
        self.client = APIClient()
        self.user = User.objects.create(**self._user_creds)
        self.tocken = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.tocken)

    def test_student_list(self):
        """Test the student list endpoint."""
        response = self.client.get('/api/v1/students/')
        self.assertEqual(response.status_code, HTTP_STATUS_OK)

    def test_student_create(self):
        """Test the student creation endpoint."""
        student_data = {
            'first_name': 'Student 1',
            'last_name': 'Noskov',
            'date_of_receipt': '2023-12-12',
        }
        response = self.client.post('/api/v1/students/', student_data)
        self.assertEqual(response.status_code, HTTP_STATUS_CREATED)
        self.assertIn('id', response.data)
        self.assertIn(response.data['id'], [str(student.id) for student in Student.objects.all()])

    def test_student_update(self):
        """Test the student update endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        student_id = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=superuser,
        ).id

        student_data = {
            'first_name': 'Student 11',
            'last_name': 'Noskov',
            'date_of_receipt': '2022-12-12',
        }
        response = self.client.put(f'/api/v1/students/{student_id}/', student_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertIn('id', response.data)

        updated_student = Student.objects.get(first_name='Student 11')
        expected_date = datetime.datetime.strptime('2022-12-12', '%Y-%m-%d').date()

        self.assertEqual(updated_student.date_of_receipt, expected_date)
        self.assertEqual(updated_student.last_name, 'Noskov')
        self.assertEqual(Student.objects.get(last_name='Noskov').date_of_receipt, expected_date)

    def test_student_delete(self):
        """Test student delete endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=superuser,
        ).id

        response = self.client.delete(f'/api/v1/students/{student}/')
        self.assertEqual(response.status_code, HTTP_STATUS_NO_CONTENT)


class TestReview(TestCase):
    """Test case for the Review model."""

    _user_creds = {'username': 'abc', 'password': '123'}

    def setUp(self):
        """Set up the test environment for each test in this test case."""
        self.client = APIClient()
        self.user = User.objects.create(**self._user_creds)
        self.tocken = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.tocken)

    def test_review_list(self):
        """Test the review list endpoint."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, HTTP_STATUS_OK)

    def test_reviews_create(self):
        """Test the review creation endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        course_id = Course.objects.create(title='Course 1', description='course1', user=superuser).id
        student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=superuser,
        ).id

        review_data = {
            'course': course_id,
            'student': student,
            'review_text': 'Review 1',
            'grade': 5,
        }
        response = self.client.post('/api/v1/reviews/', review_data)
        self.assertEqual(response.status_code, HTTP_STATUS_CREATED)
        self.assertIn('id', response.data)
        self.assertIn(response.data['id'], [str(review.id) for review in Review.objects.all()])

    def test_review_update(self):
        """Test the review update endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        course = Course.objects.create(title='Course 1', description='course1', user=superuser)
        student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=superuser,
        )
        review_id = Review.objects.create(course=course, review_text='Review 1', student=student).id

        review_data = {
            'course': course.id,
            'student': student.id,
            'review_text': 'Review 2',
            'grade': 5,
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}/', review_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertIn('id', response.data)

        updated_review = Review.objects.get(review_text='Review 2')
        self.assertEqual(updated_review.course, course)
        self.assertEqual(updated_review.grade, 5)
        self.assertEqual(updated_review.student, student)

    def test_review_delete(self):
        """Test the review delete endpoint."""
        superuser = User.objects.create_superuser(username='superuser', password='password')
        self.client.force_authenticate(user=superuser, token=Token.objects.create(user=superuser))
        course = Course.objects.create(title='Course 1', description='course1', user=superuser)
        student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=superuser,
        )
        review = Review.objects.create(course=course, review_text='Review 1', student=student)

        response = self.client.delete(f'/api/v1/reviews/{review.id}/')
        self.assertEqual(response.status_code, HTTP_STATUS_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=review.id).exists())


class ReviewFormTest(TestCase):
    """Test case for the ReviewForm."""

    def setUp(self):
        """Set up the test case with a user and a student."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=self.user,
        )

    def test_form(self):
        """Test the validity of the ReviewForm."""
        form_data = {'review_text': 'Great course!', 'grade': 5, 'student': self.student.id}
        form = ReviewForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())


class CourseModelTest(TestCase):
    """Test case for the Course model."""

    def test_str_course(self):
        """Test the string representation of the Course model."""
        course = Course(title='Test Course', description='This is a test course.')
        self.assertEqual(str(course), 'Test Course')


class StudentModelTest(TestCase):
    """Test case for the Student model."""

    def test_str_student(self):
        """Test the string representation of the Student model."""
        student = Student(first_name='John', last_name='Doe', date_of_receipt=datetime.date.today())
        self.assertEqual(str(student), 'John')


class CourseToStudentModelTest(TestCase):
    """Test case for the CourseToStudent model."""

    def test_str_coursetostudent(self):
        """Test the string representation of the CourseToStudent model."""
        user = User.objects.create_user(username='testuser', password='12345')
        course = Course.objects.create(title='Test Course', description='This is a test course.', user=user)
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_receipt=datetime.date.today(),
            user=user,
        )
        course_to_student = CourseToStudent.objects.create(course=course, student=student)
        self.assertEqual(str(course_to_student), 'Test Course to John')


class ReviewModelTest(TestCase):
    """Test case for the Review model."""

    def test_str(self):
        """Test the string representation of the Review model."""
        user = User.objects.create_user(username='testuser', password='12345')
        course = Course.objects.create(title='Test Course', description='This is a test course.', user=user)
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_receipt=datetime.date.today(),
            user=user,
        )
        review = Review.objects.create(course=course, student=student, review_text='Great course!', grade=5)
        self.assertEqual(str(review), 'Review for Test Course by John')


class UserRegistrationViewTest(TestCase):
    """Test case for the user registration view."""

    def setUp(self):
        """Set up the test case with a client and register URL."""
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_success(self):
        """Test successful user registration."""
        user_data = {'username': 'testuser', 'password1': '12345', 'password2': '12345'}
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_passwords_dont_match(self):
        """Test user registration with mismatched passwords."""
        user_data = {'username': 'testuser', 'password1': '12345', 'password2': '54321'}
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Пароли не совпадают!')

    def test_register_user_already_exists(self):
        """Test user registration with an already existing username."""
        User.objects.create_user(username='testuser', password='12345')
        user_data = {'username': 'testuser', 'password1': '12345', 'password2': '12345'}
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует!')


class UserLoginViewTest(TestCase):
    """Test case for the user login view."""

    def setUp(self):
        """Set up the test case with a client, login URL, and a user."""
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_success(self):
        """Test successful user login."""
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_no_username_or_password(self):
        """Test user login with no username or password."""
        response = self.client.post(self.login_url, {'username': '', 'password': ''})
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Имя пользователя и пароль обязательны для заполнения!')

    def test_login_user_not_found(self):
        """Test user login with a non-existing username."""
        response = self.client.post(self.login_url, {'username': 'wronguser', 'password': '12345'})
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Пользователь не найден!')

    def test_login_wrong_password(self):
        """Test user login with a wrong password."""
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Введен неверный пароль!')


class LogOutViewTest(TestCase):
    """Test case for the logout view."""

    def setUp(self):
        """Set up the test case with a client, logout URL, and a logged-in user."""
        self.client = Client()
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_logout(self):
        """Test user logout."""
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class CreateStudentViewTest(TestCase):
    """Test case for the student creation view."""

    def setUp(self):
        """Set up the test case with a client, create student URL, and user."""
        self.client = Client()
        self.create_student_url = reverse('create_student')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_student_success(self):
        """Test successful student creation."""
        test_data = {
            'first_name': 'Test',
            'last_name': 'Student',
            'date_of_receipt': datetime.date.today(),
        }
        response = self.client.post(self.create_student_url, test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertTrue(Student.objects.filter(user=self.user).exists())

    def test_create_student_already_exists(self):
        """Test student creation with an already existing student."""
        Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            date_of_receipt=datetime.date.today(),
        )
        test_data = {
            'first_name': 'Test',
            'last_name': 'Student',
            'date_of_receipt': datetime.date.today(),
        }
        response = self.client.post(self.create_student_url, test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы уже создали студента!')

    def test_create_student_future_date_of_receipt(self):
        """Test student creation with a future date of receipt."""
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        test_data = {
            'first_name': 'Test',
            'last_name': 'Student',
            'date_of_receipt': future_date,
        }
        response = self.client.post(self.create_student_url, test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Дата поступления не может быть в будущем!')


class EditStudentViewTest(TestCase):
    """Test case for the student editing view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, and student."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            date_of_receipt=datetime.date.today(),
        )
        self.client.login(username='testuser', password='12345')

    def test_edit_student_success(self):
        """Test successful student editing."""
        test_data = {
            'first_name': 'New',
            'last_name': 'Student',
            'date_of_receipt': datetime.date.today(),
        }
        response = self.client.post(reverse('edit_student', args=[self.student.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'New')
        self.assertEqual(self.student.last_name, 'Student')

    def test_edit_student_not_owner(self):
        """Test student editing by a user who is not the owner."""
        self.client.login(username='otheruser', password='12345')
        test_data = {
            'first_name': 'New',
            'last_name': 'Student',
            'date_of_receipt': datetime.date.today(),
        }
        response = self.client.post(reverse('edit_student', args=[self.student.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы можете редактировать только своего студента!')

    def test_edit_student_future_date_of_receipt(self):
        """Test student editing with a future date of receipt."""
        future_date = datetime.date.today() + datetime.timedelta(days=1)
        test_data = {
            'first_name': 'New',
            'last_name': 'Student',
            'date_of_receipt': future_date,
        }
        response = self.client.post(reverse('edit_student', args=[self.student.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Дата поступления не может быть в будущем!')


class DeleteStudentViewTest(TestCase):
    """Test case for the student deletion view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, and student."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='Student',
            date_of_receipt=datetime.date.today(),
        )
        self.client.login(username='testuser', password='12345')

    def test_delete_student_success(self):
        """Test successful student deletion."""
        response = self.client.post(reverse('delete_student', args=[self.student.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())


class CreateCourseViewTest(TestCase):
    """Test case for the course creation view."""

    def setUp(self):
        """Set up the test case with a client, create course URL, and user."""
        self.client = Client()
        self.create_course_url = reverse('create_course')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_course_success(self):
        """Test successful course creation."""
        test_data = {
            'title': 'Test Course',
            'description': 'This is a test course.',
        }
        response = self.client.post(self.create_course_url, test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertTrue(Course.objects.filter(user=self.user).exists())

    def test_create_course_unauthenticated(self):
        """Test course creation by an unauthenticated user."""
        self.client.logout()
        test_data = {
            'title': 'Test Course',
            'description': 'This is a test course.',
        }
        response = self.client.post(self.create_course_url, test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertRedirects(response, '/login/?next=/create_course/')


class EditCourseViewTest(TestCase):
    """Test case for the course editing view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, and course."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.course = Course.objects.create(
            user=self.user,
            title='Test Course',
            description='This is a test course.',
        )
        self.client.login(username='testuser', password='12345')

    def test_edit_course_success(self):
        """Test successful course editing."""
        test_data = {
            'title': 'New Course',
            'description': 'This is a new course.',
        }
        response = self.client.post(reverse('edit_course', args=[self.course.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'New Course')
        self.assertEqual(self.course.description, 'This is a new course.')

    def test_edit_course_not_owner(self):
        """Test course editing by a user who is not the owner."""
        self.client.login(username='otheruser', password='12345')
        test_data = {
            'title': 'New Course',
            'description': 'This is a new course.',
        }
        response = self.client.post(reverse('edit_course', args=[self.course.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы можете редактировать только свой курс!')
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Test Course')
        self.assertEqual(self.course.description, 'This is a test course.')


class DeleteCourseViewTest(TestCase):
    """Test case for the course deletion view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, and course."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.course = Course.objects.create(user=self.user, title='Test Course', description='This is a test course.')
        self.client.login(username='testuser', password='12345')

    def test_delete_course_success(self):
        """Test successful course deletion."""
        response = self.client.post(reverse('delete_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())


class EditReviewViewTest(TestCase):
    """Test case for the review editing view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, course, student, and review."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.course = Course.objects.create(
            user=self.user,
            title='Test Course',
            description='This is a test course.',
        )
        self.student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=self.user,
        )
        self.review = Review.objects.create(
            course=self.course,
            review_text='Great course!',
            grade=5,
            student=self.student,
        )
        self.client.login(username='testuser', password='12345')

    def test_edit_review_success(self):
        """Test successful review editing."""
        test_data = {
            'review_text': 'New review!',
            'grade': 4,
        }
        response = self.client.post(reverse('edit_review', args=[self.review.id]), test_data)
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.review.refresh_from_db()
        self.assertEqual(self.review.review_text, 'New review!')
        self.assertEqual(self.review.grade, 4)


class EnrollCourseViewTest(TestCase):
    """Test case for the course enrollment view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, course, and student."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='12345',
        )
        self.course = Course.objects.create(
            user=self.user,
            title='Test Course',
            description='This is a test course.',
        )
        self.student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=self.user,
        )
        self.client.login(username='testuser', password='12345')

    def test_enroll_course_success(self):
        """Test successful course enrollment."""
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertTrue(CourseToStudent.objects.filter(student=self.student, course=self.course).exists())

    def test_enroll_course_already_enrolled(self):
        """Test course enrollment when already enrolled."""
        CourseToStudent.objects.create(student=self.student, course=self.course)
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы уже поступили на этот курс')

    def test_enroll_course_not_student(self):
        """Test course enrollment by a user who is not a student."""
        self.client.login(username='otheruser', password='12345')
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы должны быть зарегистрированы как студент, чтобы поступить на курс')


class UnenrollCourseViewTest(TestCase):
    """Test case for the course unenrollment view."""

    def setUp(self):
        """Set up the test case with a client, user, other user, course, student, and course enrollment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='12345',
        )
        self.course = Course.objects.create(
            user=self.user,
            title='Test Course',
            description='This is a test course.',
        )
        self.student = Student.objects.create(
            first_name='Student 1',
            last_name='Noskov',
            date_of_receipt='2022-12-12',
            user=self.user,
        )
        self.course_to_student = CourseToStudent.objects.create(
            student=self.student,
            course=self.course,
        )
        self.client.login(username='testuser', password='12345')

    def test_unenroll_course_success(self):
        """Test successful course unenrollment."""
        response = self.client.post(reverse('unenroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_FOUND)
        self.assertFalse(CourseToStudent.objects.filter(student=self.student, course=self.course).exists())

    def test_unenroll_course_already_unenrolled(self):
        """Test course unenrollment when already unenrolled."""
        self.course_to_student.delete()
        response = self.client.post(reverse('unenroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertContains(response, 'Вы уже покинули этот курс')


class ViewsTest(TestCase):
    """Test case for the views."""

    def setUp(self):
        """Set up the test case with a client."""
        self.client = Client()

    def test_students_view(self):
        """Test the students view."""
        response = self.client.get(reverse('students'))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertTemplateUsed(response, 'students.html')

    def test_courses_view(self):
        """Test the courses view."""
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertTemplateUsed(response, 'courses.html')

    def test_reviews_view(self):
        """Test the reviews view."""
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertTemplateUsed(response, 'reviews.html')

    def test_coursetostudents_view(self):
        """Test the coursestostudents view."""
        response = self.client.get(reverse('coursestostudents'))
        self.assertEqual(response.status_code, HTTP_STATUS_OK)
        self.assertTemplateUsed(response, 'coursestostudents.html')
