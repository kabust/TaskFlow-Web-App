from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Position, Project, TaskType, Task


class PositionModelTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="QA")
        self.assertEqual(str(position), position.name)


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test project")
        position = Position.objects.create(name="QA")
        pm_position = Position.objects.create(name="Project Manager")

        for i in range(5):
            get_user_model().objects.create_user(
                username=f"worker{i}",
                password="qwerty1234",
                project=self.project,
                position=position,
            )

        get_user_model().objects.create_user(
            username="project_manager",
            password="qwerty1234",
            project=self.project,
            position=pm_position,
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_get_project_managers(self):
        self.assertEqual(
            self.project.get_project_managers().first(),
            get_user_model()
            .objects.filter(
                project=self.project,
                position__name="Project Manager"
            )
            .first(),
        )

    def test_get_all_workers(self):
        self.assertEqual(
            self.project.get_all_workers().count(),
            get_user_model().objects.filter(project=self.project).count(),
        )


class TaskTypeModelTest(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Test")
        self.assertEqual(str(task_type), task_type.name)


class TaskModelTest(TestCase):
    def setUp(self):
        position = Position.objects.create(name="QA")
        project = Project.objects.create(name="Test project")
        for i in range(3):
            get_user_model().objects.create_user(
                username=f"worker{i}",
                password="qwerty1234",
                position=position,
                project=project
            )

        self.task = Task.objects.create(
            name="Test task",
            description="Cool description",
            deadline=datetime.today().date(),
            priority="Urgent",
            project=project
        )
        self.task.assignees.set(get_user_model().objects.all())

    def test_task_str(self):
        self.assertEqual(
            str(self.task),
            f"{self.task.name} ({str(self.task.priority)} "
            f"/ finish before {self.task.deadline})",
        )

    def test_past_deadline(self):
        self.assertEqual(self.task.past_deadline(), 0)
