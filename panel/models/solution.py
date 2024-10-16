from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from .task import Task


class Solution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    solution_file = models.FileField(upload_to='solutions/', null=True, blank=True)
    test_results = models.JSONField(null=True, blank=True)
    tests_passed = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"Solution for {self.task.title} by {self.user.username}"
