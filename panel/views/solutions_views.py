import uuid

from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from ..forms import SolutionForm
from django.contrib.auth.decorators import login_required

from ..forms.task_form import TaskForm
from ..forms.text_case_form import TestCaseForm
from ..functions import run_tests, count_stats, count_table
from ..models import Solution, Task, GroupMembership, TestCase
import os
import json


@login_required
def show_solution(request, solution_id):
    solution = Solution.objects.get(id=solution_id)
    user = solution.user
    task = solution.task
    with open(solution.solution_file.path, 'r') as file:
        solution_code = file.read()

    return render(request, 'panel/solution.html', {
        'solution': solution,
        'user': user,
        'task': task,
        'solution_code': solution_code,
        'test_results': solution.test_results
    })


@login_required
@require_http_methods(["POST"])
def update_points(request, solution_id):
    points = request.POST.get('points')
    solution = Solution.objects.get(id=solution_id)
    points = int(points)
    if points <= solution.task.max_points:
        solution.points = points
        solution.save()
        messages.info(request, 'Points updated successfully.')
    else:
        messages.error(request, f'Points cannot exceed the maximum of {solution.task.max_points}.')
    return redirect('submit_solution', task_id=solution.task.id)


@login_required
def submit_solution(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user

    if task.group.creator == user:
        user_role = 'OWNER'
    else:
        membership = GroupMembership.objects.filter(user=user, group=task.group).first()
        if not membership:
            messages.error(request, "It's not your task.")
            return redirect('dashboard')
        user_role = membership.role

    previous_solutions = Solution.objects.filter(user=user, task_id=task_id)
    if previous_solutions.exists():
        last_solution = previous_solutions.latest('submitted_at')
        with open(os.path.join(settings.MEDIA_ROOT, last_solution.solution_file.name), 'r') as file:
            default_code = file.read()
    else:
        default_code = task.function_starter

    if request.method == 'POST':
        if task.end_date and task.end_date < timezone.now():
            messages.error(request, "You can no longer submit a solution for this task..")
            return redirect('dashboard')
        if task.max_attempts and Solution.objects.filter(user=user, task=task).count() >= task.max_attempts:
            messages.error(request, "You can no longer submit a solution for this task..")
            return redirect('dashboard')

        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            solution_type = form.cleaned_data['solution_type']
            if solution_type == 'text':
                python_code = form.cleaned_data['python_code']
                filename = f'solutions/{uuid.uuid1()}.py'
                file_path = os.path.join(settings.MEDIA_ROOT, filename)

                with open(file_path, 'w') as file:
                    file.write(python_code)

                solution = Solution(
                    user=user,
                    task=task,
                    solution_file=filename
                )
                solution.save()
            else:
                solution = form.save()

            results = run_tests(request, solution)
            solution.test_results = results
            solution.save()

            # Show notification in plagiarism page
            task.is_solutions_changed = True
            task.save()

            return redirect('submit_solution', task_id=solution.task.id)
    else:
        form = SolutionForm(initial={'task': task_id, 'user': request.user, 'python_code': default_code})

    previous_solutions = Solution.objects.filter(user=user, task_id=task_id)
    stats = count_stats(previous_solutions)
    ranking_table = count_table(task)

    task_form = TaskForm(instance=task)
    test_case_form = TestCaseForm()

    return render(request, 'panel/submit_solution.html', {
        'task': task,
        'form': form,
        'task_form': task_form,
        'test_case_form': test_case_form,
        'test_cases': TestCase.objects.filter(task_id=task_id),
        'task_id': task_id,
        'previous_solutions': previous_solutions,
        'user': user,
        'stats': stats,
        'user_role': user_role,
        'ranking_table': ranking_table
    })
