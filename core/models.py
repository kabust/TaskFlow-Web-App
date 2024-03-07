from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position, on_delete=models.SET_NULL, null=True, blank=True
    )
    project = models.ForeignKey(
        to="Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ("username",)


class Project(models.Model):
    name = models.CharField(max_length=255)

    def get_project_managers(self):
        return get_user_model().objects.filter(
            project=self, position__name="Project Manager"
        )

    def get_all_workers(self):
        return get_user_model().objects.filter(project=self)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    priorities = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="tasks")
    is_completed = models.BooleanField(blank=True, default=False)
    priority = models.CharField(max_length=255, choices=priorities)
    task_type = models.ForeignKey(
        to=TaskType, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    assignees = models.ManyToManyField(to=get_user_model(), related_name="tasks")

    def past_deadline(self):
        past = self.deadline - date.today()
        if past.days <= -1:
            return abs(past.days)
        return 0

    def get_comments(self):
        return Comment.objects.filter(task_id=self.id)

    class Meta:
        ordering = ("deadline",)

    def __str__(self):
        return f"{self.name} ({str(self.priority)} " f"/ finish before {self.deadline})"


class Comment(models.Model):
    commentator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return (
            f"Comment by {self.commentator}:\n"
            f"{self.content[:20]}"
        )
