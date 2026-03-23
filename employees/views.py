from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator

from .models import Employee


def home(request):
    employees = Employee.objects.prefetch_related("skills", "images")

    last_employees = employees.order_by("-hire_date")[:4]
    count = employees.count()

    return render(
        request,
        "home.html",
        {
            "employees": last_employees,  # ← показываем только 4 последних
            "count": count,
        },
    )


def employee_list(request):
    employees = Employee.objects.prefetch_related("skills", "images")

    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "employee_list.html", {"page_obj": page_obj})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(
        Employee.objects.prefetch_related("skills", "images"), pk=pk
    )

    days_worked = 0
    if employee.hire_date:
        days_worked = (now().date() - employee.hire_date).days

    images = employee.images.all().order_by("order")
    first_image = images.first()

    return render(
        request,
        "employee_detail.html",
        {
            "employee": employee,
            "days_worked": days_worked,
            "first_image": first_image,
            "images": images[1:],  # галерея без первого фото
        },
    )