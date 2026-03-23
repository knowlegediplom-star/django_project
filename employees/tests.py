from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Employee, Skill


class EmployeeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='12345')
        self.skill = Skill.objects.create(name='backend')

        self.employee = Employee.objects.create(
            user=self.user,
            first_name='Иван',
            last_name='Иванов',
            skill_level=5,
            description='Тест'
        )
        self.employee.skills.add(self.skill)

    # 🔹 ТЕСТ 1 — доступ к главной странице
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # 🔹 ТЕСТ 2 — список сотрудников
    def test_employee_list(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)

    # 🔹 ТЕСТ 3 — контекст
    def test_employee_context(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)

    # 🔹 ТЕСТ 4 — доступ без логина
    def test_employee_detail_unauthorized(self):
        response = self.client.get(f'/employees/{self.employee.id}/')
        self.assertNotEqual(response.status_code, 200)