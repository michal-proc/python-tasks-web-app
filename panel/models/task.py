from django.db import models

from .group import Group


class Task(models.Model):
    title = models.CharField(max_length=128)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')
    function_name = models.CharField(max_length=128)
    function_starter = models.TextField(null=True, blank=True)
    description = models.TextField()
    max_attempts = models.IntegerField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    max_points = models.IntegerField(default=10)
    is_plagiarism_checked = models.BooleanField(default=False)
    is_solutions_changed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    input_data = models.TextField(null=True, blank=True)
    expected_output = models.TextField()

    def __str__(self):
        return f"Test case for {self.task.title}"
