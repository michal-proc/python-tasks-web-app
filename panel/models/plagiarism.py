from django.db import models

from . import Solution
from .task import Task


class Plagiarism(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='plagiarisms')
    solution_one = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='plagiarisms_as_solution_one')
    solution_second = models.ForeignKey(Solution, on_delete=models.CASCADE,
                                        related_name='plagiarisms_as_solution_second')
    similarity_score = models.FloatField(default=0)
