from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    assignees = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ("deadline",)

    def __str__(self):
        return f"{self.name} ({str(self.priority)} / finish before {self.deadline})"


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(to=Position, on_delete=models.SET_NULL, null=True, blank=True)
