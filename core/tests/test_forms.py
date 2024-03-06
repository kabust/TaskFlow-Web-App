from django.contrib.auth import get_user_model
from django.test import TestCase

from core.forms import WorkerCreateForm, WorkerNameSearch, TaskForm, TaskFiltersSearch
from core.models import Project, TaskType


class TestWorkerForms(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="cool project")

    def test_worker_create_form(self):
        form_data = {
            "username": "new_user",
            "password1": "Qwerty12345!",
            "password2": "Qwerty12345!",
            "project": self.project,
            "first_name": "tester",
            "last_name": "bob"
        }
        form = WorkerCreateForm(form_data)
        self.assertTrue(form.is_valid())

    def test_worker_search_form_with_args(self):
        form_data = {
            "username": "user1",
        }
        form = WorkerNameSearch(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_search_form_without_args(self):
        form_data = {
            "username": "",
        }
        form = WorkerNameSearch(data=form_data)
        self.assertTrue(form.is_valid())


class TestTaskForms(TestCase):
    def test_task_filters_search(self):
        form_data = {
            "filters": ["past_dl", "urgent", "done"]
        }
        form = TaskFiltersSearch(data=form_data)
        self.assertTrue(form.is_valid())
