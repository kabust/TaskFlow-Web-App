from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from core.forms import WorkerCreationForm, WorkerNameSearch, TaskFiltersSearch
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
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
        filters = self.request.GET.getlist("filters")
        print(queryset)

        if "past_dl" in filters:
            queryset = queryset.filter(deadline__lt=date.today())

        if "done" in filters:
            queryset = queryset.filter(is_completed=True)

        if "urgent" in filters:
            queryset = queryset.filter(priority="Urgent")

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        filters = self.request.GET.getlist("filters")
        context["filters"] = TaskFiltersSearch(initial={"filters": filters})

        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = get_user_model().objects.all()

        if name:
            return queryset.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerNameSearch(initial={"name": name})

        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks")


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:index")
