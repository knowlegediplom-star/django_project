def employee_to_dict(employee):
    return {
        "id": employee.id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "skill_level": employee.skill_level,
        "description": employee.description,
        "skills": [s.name for s in employee.skills.all()],
    }