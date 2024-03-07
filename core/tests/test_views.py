from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import Project, Task


class IndexTest(TestCase):
    def setUp(self):
        project = Project.objects.create(name="cool project")
        self.user = get_user_model().objects.create(
            username="user1", password="top_user", project=project
        )
        self.client.force_login(self.user)

        for i in range(5):
            worker = get_user_model().objects.create_user(
                username=f"worker{i}", password="qwerty1234", project=project
            )
            task = Task.objects.create(
                name=f"task{i}",
                description="tast description",
                deadline=datetime.today(),
                project=project,
                priority="Low",
            )
            task.assignees.set((worker,))

        task = Task.objects.last()
        task.is_completed = True
        task.save()

    def test_index_counters(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.context["workers_amount"], 6)
        self.assertEqual(response.context["tasks_todo_amount"], 4)
        self.assertEqual(response.context["tasks_done"], 1)
