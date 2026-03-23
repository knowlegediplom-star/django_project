from django.db import models
from employees.models import Employee

class Workplace(models.Model):
    desk_number = models.IntegerField()
    info = models.TextField(blank=True)

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Стол {self.desk_number}"