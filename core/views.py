from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from core.forms import WorkerCreationForm
from core.models import Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    workers_amount = Worker.objects.count()
    tasks_amount = Task.objects.count()

    context = {
        "workers_amount": workers_amount,
        "tasks_amount": tasks_amount,
    }
    return render(request, "core/index.html", context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    paginate_by = 5


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks")


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:index")
