from django.urls import path

from core.views import (
    index,
    TaskListView,
    TaskDetailView,
    WorkerDetailView,
    WorkerListView,
    WorkerCreateView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerUpdateView
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"
    ),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "accounts/register/", WorkerCreateView.as_view(), name="worker-create"
    ),
]

app_name = "core"
