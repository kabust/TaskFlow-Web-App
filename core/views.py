from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin

from core.forms import (
    WorkerNameSearch,
    TaskFiltersSearch,
    TaskForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    CommentForm,
)
from core.models import Task, Project, Comment


@login_required
def index(request: HttpRequest) -> HttpResponse:
    workers_amount = (
        get_user_model().objects.filter(project=request.user.project).count()
    )
    tasks_todo_amount = Task.objects.filter(
        project=request.user.project, is_completed=False
    ).count()
    tasks_done = Task.objects.filter(
        is_completed=True, project=request.user.project
    ).count()
    if request.user.date_joined.date() != date.today():
        daily_refresher = request.session.get("daily_refresher", None)
        if not daily_refresher:
            request.session["daily_refresher"] = 1
        request.session.set_expiry(86400)
    else:
        daily_refresher = 1

    context = {
        "workers_amount": workers_amount,
        "tasks_todo_amount": tasks_todo_amount,
        "tasks_done": tasks_done,
        "daily_refresher": daily_refresher,
    }

    return render(request, "core/index.html", context)


class TaskListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5

    def get_queryset(self):
        queryset = Task.objects.prefetch_related("assignees")
        project_id = self.request.GET.get("project_id")
        queryset = queryset.filter(project_id=project_id)
        filters = self.request.GET.getlist("filters")

        if "past_dl" in filters:
            queryset = queryset.filter(deadline__lt=date.today())

        if "urgent" in filters:
            queryset = queryset.filter(priority="Urgent")

        if "done" in filters:
            queryset = queryset.filter(is_completed=True)
        else:
            queryset = queryset.filter(is_completed=False)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        filters = self.request.GET.getlist("filters")
        context["filters"] = TaskFiltersSearch(initial={"filters": filters, "project_id": project_id})
        context["project"] = Project.objects.get(id=project_id)

        return context


class TaskDetailView(FormMixin, generic.DetailView):
    model = Task
    form_class = CommentForm

    def get_success_url(self):
        return reverse("core:task-detail", args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        context["form"] = CommentForm(
            initial={"task": self.object, "commentator": self.request.user}
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def delete_comment(
    request: HttpRequest, task_pk: int, com_pk: int
) -> HttpResponseRedirect | HttpResponse:
    comment = Comment.objects.get(pk=com_pk)
    task_project = Task.objects.get(pk=task_pk).project
    if (request.user != comment.commentator or
            request.user.project != task_project):
        return HttpResponse("Unauthorized", status=401)
    comment.delete()
    return HttpResponseRedirect(reverse("core:task-detail", args=(task_pk,)))


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        return reverse("core:task-list") + f"?project_id={self.request.user.project.id}"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        obj = super().get_object()

        if (not self.request.user.project or
                obj.project != self.request.user.project):
            return HttpResponse("Unauthorized", status=401)

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("core:task-list") + f"?project_id={self.request.user.project.id}"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task

    def get(self, request, *args, **kwargs):
        obj = super().get_object()

        if (not self.request.user.project or
                obj.project != self.request.user.project):
            return HttpResponse("Unauthorized", status=401)

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("core:task-list", args=(self.get_object().project.id,))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


def toggle_completed(
        request: HttpRequest, pk
) -> HttpResponseRedirect | HttpResponse:
    task = Task.objects.get(pk=pk)

    if request.user in task.assignees.all():
        task.is_completed = not task.is_completed
        task.save()
    else:
        return HttpResponse("Unauthorized", status=401)

    return HttpResponseRedirect(reverse("core:task-detail", args=(pk,)))


class WorkerListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10

    def get_queryset(self):
        name = self.request.GET.get("name")
        queryset = get_user_model().objects.all()

        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        if self.request.GET.get("user_project") == "true":
            queryset = queryset.filter(project=self.request.user.project)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        user_project = self.request.GET.get("user_project", "")
        context["search_form"] = WorkerNameSearch(initial={"name": name, "user_project": user_project})
        context["num_workers"] = self.get_queryset().count()
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = get_user_model().objects.prefetch_related("tasks")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("core:index")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class WorkerUpdateView(generic.UpdateView):
    form_class = WorkerUpdateForm

    def get_queryset(self):
        user = get_user_model().objects.filter(pk=self.request.user.pk)
        return user

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("core:worker-detail", args=(pk,))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.project:
            context["users_project"] = self.request.user.project.pk
        return context
