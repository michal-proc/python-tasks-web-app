from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from common import settings
from panel.functions import PlagiarismChecker
from panel.models import Solution, Task, Plagiarism

import os


@login_required
def check_plagiarism(request, task_id):
    task = Task.objects.get(id=task_id)
    solutions = Solution.objects.filter(task=task).order_by('-submitted_at')

    # Delete all existing
    plagiarisms = Plagiarism.objects.filter(task=task)
    plagiarisms.delete()

    latest_solutions = {}

    for solution in solutions:
        if solution.user not in latest_solutions:
            latest_solutions[solution.user] = solution

    active_solutions = list(latest_solutions.values())

    for checked_solution in active_solutions:
        for other_solution in active_solutions:
            if checked_solution.id != other_solution.id:
                with (open(os.path.join(settings.MEDIA_ROOT, checked_solution.solution_file.name), 'r') as check_file,
                      open(os.path.join(settings.MEDIA_ROOT, other_solution.solution_file.name), 'r') as other_file):

                    calculated_plagiarism = PlagiarismChecker.calculate_plagiarism(check_file.read(), other_file.read())
                    combined_similarity = int(calculated_plagiarism["combined_similarity"] * 100)

                    # Save the plagiarism result to the database
                    Plagiarism.objects.create(
                        task=task,
                        solution_one=checked_solution,
                        solution_second=other_solution,
                        similarity_score=combined_similarity
                    )

    # Show notification in plagiarism page
    task.is_plagiarism_checked = True
    task.is_solutions_changed = True
    task.save()

    return redirect('submit_solution', task_id=task.id)


@login_required
def show_plagiarism(request, task_id):
    task = Task.objects.get(id=task_id)
    plagiarisms = Plagiarism.objects.filter(task=task)

    return render(request, 'panel/view_plagiarisms.html', {
        'task': task,
        'plagiarisms': plagiarisms,
    })
