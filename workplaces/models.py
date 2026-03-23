from django.db import models
from employees.models import Employee
from django.core.exceptions import ValidationError


class Workplace(models.Model):
    desk_number = models.IntegerField()
    info = models.TextField(blank=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    def clean(self):
        # если сотрудник не выбран — не проверяем
        if not self.employee:
            return

        employee_skills = list(self.employee.skills.values_list("name", flat=True))

        # соседи (стол -1 и +1)
        neighbors = Workplace.objects.filter(
            desk_number__in=[self.desk_number - 1, self.desk_number + 1]
        )

        for neighbor in neighbors:
            # защита если вдруг нет сотрудника
            if not neighbor.employee:
                continue

            neighbor_skills = list(
                neighbor.employee.skills.values_list("name", flat=True)
            )

            # ❗ проверка: тестировщик рядом с разработчиком
            if "testing" in neighbor_skills and (
                "frontend" in employee_skills or "backend" in employee_skills
            ):
                raise ValidationError(
                    "Нельзя сажать разработчиков рядом с тестировщиками"
                )

            if ("frontend" in neighbor_skills or "backend" in neighbor_skills) and (
                "testing" in employee_skills
            ):
                raise ValidationError(
                    "Нельзя сажать тестировщиков рядом с разработчиками"
                )

    def __str__(self):
        return f"Стол {self.desk_number}"