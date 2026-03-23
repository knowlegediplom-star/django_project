from django.contrib import admin
from .models import Employee, Skill

admin.site.register(Employee)
admin.site.register(Skill)
from .models import EmployeeImage

admin.site.register(EmployeeImage)