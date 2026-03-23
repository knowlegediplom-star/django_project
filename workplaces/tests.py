from django.test import TestCase
from django.contrib.auth.models import User
from employees.models import Employee, Skill
from .models import Workplace
from django.core.exceptions import ValidationError


class WorkplaceValidatorTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="dev", password="123")
        self.user2 = User.objects.create_user(username="tester", password="123")

        self.skill_dev = Skill.objects.create(name="frontend")
        self.skill_test = Skill.objects.create(name="testing")

        self.employee1 = Employee.objects.create(
            user=self.user1,
            first_name="Dev",
            last_name="One",
            skill_level=5,
            description="dev",
        )
        self.employee1.skills.add(self.skill_dev)

        self.employee2 = Employee.objects.create(
            user=self.user2,
            first_name="Test",
            last_name="Two",
            skill_level=5,
            description="tester",
        )
        self.employee2.skills.add(self.skill_test)

    def test_validator(self):
        Workplace.objects.create(desk_number=1, employee=self.employee1)

        workplace = Workplace(desk_number=2, employee=self.employee2)

        with self.assertRaises(ValidationError):
            workplace.full_clean()