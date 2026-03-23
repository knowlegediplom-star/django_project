import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from .serializers import employee_to_dict


@csrf_exempt
def employee_list(request):
    if request.method == "GET":
        employees = Employee.objects.all()

        # фильтр
        skill = request.GET.get("skill")
        if skill:
            employees = employees.filter(skills__name__icontains=skill)

        # пагинация
        paginator = Paginator(employees, 10)
        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)

        data = [employee_to_dict(e) for e in page_obj]

        return JsonResponse({
            "count": paginator.count,
            "page": int(page),
            "results": data
        })

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required"}, status=403)

        data = json.loads(request.body)

        employee = Employee.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            skill_level=data.get("skill_level", 1),
            description=data.get("description", "")
        )

        return JsonResponse(employee_to_dict(employee), status=201)


@csrf_exempt
def employee_detail(request, id):
    employee = Employee.objects.filter(id=id).first()

    if not employee:
        return JsonResponse({"detail": "Not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(employee_to_dict(employee))

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required"}, status=403)

    if request.method == "PUT":
        data = json.loads(request.body)

        employee.first_name = data.get("first_name", employee.first_name)
        employee.last_name = data.get("last_name", employee.last_name)
        employee.skill_level = data.get("skill_level", employee.skill_level)
        employee.description = data.get("description", employee.description)

        employee.save()
        return JsonResponse(employee_to_dict(employee))

    if request.method == "DELETE":
        employee.delete()
        return JsonResponse({"detail": "Deleted"}, status=204)