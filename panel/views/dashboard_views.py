from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone

from ..enums.role import Role
from ..models import Group, Task, Solution, Plagiarism, GroupMembership


@login_required
def dashboard(request):
    user = request.user

    owner_groups = Group.objects.filter(creator=user).count()
    total_groups = Group.objects.filter(memberships__user=user).count() + owner_groups
    student_groups_count = Group.objects.filter(memberships__user=user, memberships__role='STUDENT').count()
    instructor_groups_count = Group.objects.filter(memberships__user=user, memberships__role='INSTRUCTOR').count()
    total_tasks = Task.objects.filter(group__memberships__user=user).count()
    tasks_with_solution = Task.objects.filter(
        group__memberships__user=user,
        id__in=Solution.objects.filter(user=user).values_list('task_id', flat=True)
    ).count()
    tasks_without_solution = Task.objects.filter(
        group__memberships__user=user
    ).exclude(
        id__in=Solution.objects.filter(user=user).values_list('task_id', flat=True)
    ).count()
    total_solutions = Solution.objects.filter(user=user).count()
    total_points = Solution.objects.filter(user=user).aggregate(total_points=Sum('points'))['total_points'] or 0
    max_points = Task.objects.filter(group__memberships__user=user).aggregate(max_points=Sum('max_points'))[
                     'max_points'] or 0

    plagiarism_detected = Plagiarism.objects.filter(
        solution_one__user=user,
        similarity_score__gte=99
    ).count()
    plagiarism_suspected = Plagiarism.objects.filter(
        solution_one__user=user,
        similarity_score__gte=95,
        similarity_score__lt=99
    ).count()

    user_groups = Group.objects.filter(memberships__user=user) | Group.objects.filter(creator=user)
    tasks = Task.objects.filter(group__in=user_groups)

    tasks_with_submission = []
    for task in tasks:
        submitted_solutions_count = Solution.objects.filter(user=user, task=task).count()
        is_submitted = submitted_solutions_count > 0

        is_active = True
        if task.end_date and task.end_date < timezone.now():
            is_active = False
        if task.max_attempts and submitted_solutions_count >= task.max_attempts:
            is_active = False

        user_role = GroupMembership.objects.filter(group=task.group, user=user).first()
        if user_role:
            user_role = user_role.role
        else:
            user_role = 'OWNER'

        tasks_with_submission.append({
            'id': task.id,
            'title': task.title,
            'group': task.group,
            'description': task.description,
            'submitted': is_submitted,
            'max_attempts': task.max_attempts if task.max_attempts else 'Unlimited',
            'end_date': task.end_date if task.end_date else 'No deadline',
            'is_active': is_active,
            'role': user_role
        })

    created_groups = Group.objects.filter(creator=user)
    instructor_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.INSTRUCTOR)
    student_groups = Group.objects.filter(memberships__user=user, memberships__role=Role.STUDENT)

    groups_with_roles = []

    for group in created_groups:
        groups_with_roles.append({'group': group, 'role': 'OWNER'})

    for group in instructor_groups:
        groups_with_roles.append({'group': group, 'role': 'INSTRUCTOR'})

    for group in student_groups:
        groups_with_roles.append({'group': group, 'role': 'STUDENT'})

    return render(request, 'panel/dashboard.html', {
        'total_groups': total_groups,
        'student_groups': student_groups_count,
        'instructor_groups': instructor_groups_count,
        'owner_groups': owner_groups,
        'total_tasks': total_tasks,
        'total_solutions': total_solutions,
        'total_points': total_points,
        'max_points': max_points,
        'plagiarism_detected': plagiarism_detected,
        'plagiarism_suspected': plagiarism_suspected,
        'tasks_with_solution': tasks_with_solution,
        'tasks_without_solution': tasks_without_solution,

        'tasks': tasks_with_submission,
        'groups': groups_with_roles
    })
