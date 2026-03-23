from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)

    skills = models.ManyToManyField(Skill)
    skill_level = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"