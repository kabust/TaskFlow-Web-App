from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(to=Position, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ("username",)


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    priorities = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low")
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(blank=True, default=False)
    priority = models.CharField(max_length=255, choices=priorities)
    task_type = models.ForeignKey(to=TaskType, on_delete=models.SET_NULL, null=True, related_name="tasks")
    assignees = models.ManyToManyField(to=get_user_model(), related_name="tasks")

    def past_deadline(self):
        past = self.deadline - date.today()
        if past.days <= -1:
            return abs(past.days)
        return 0

    class Meta:
        ordering = ("deadline",)

    def __str__(self):
        return f"{self.name} ({str(self.priority)} / finish before {self.deadline})"
