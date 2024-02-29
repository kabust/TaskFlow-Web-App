from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from core.models import Worker, Task


def index(request: HttpRequest) -> HttpResponse:
    num_workers = Worker.objects.count()

    context = {"num_workers": num_workers}
    return render(request, "core/index.html", context)


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
