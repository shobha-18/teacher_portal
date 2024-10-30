from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student, Teacher

class PortalTests(TestCase):
    def setUp(self):
        self.teacher_user = get_user_model().objects.create_user(username='testteacher', password='pass123')
        self.teacher = Teacher.objects.create(user=self.teacher_user)  
        self.client.login(username='testteacher', password='pass123')

    def test_login(self):
        response = self.client.post(reverse('login_view'), {'username': 'testteacher', 'password': 'pass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login_view'))

    def test_add_student(self):
        response = self.client.post(reverse('add_student'), {
            'name': 'John Doe',
            'subject': 'Math',
            'marks': 80
        })
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.first().name, 'John Doe')

    def test_edit_student(self):
        student = Student.objects.create(name='Jane Doe', subject='Science', marks=85, teacher=self.teacher)
        response = self.client.post(reverse('edit_student', args=[student.id]), {
            'name': 'Jane Doe',
            'subject': 'Science',
            'marks': 90
        })
        student.refresh_from_db()
        self.assertEqual(student.marks, 90)
