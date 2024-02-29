from django.urls import path

from core.views import index, TaskListView, TaskDetailView, WorkerDetailView, WorkerListView, WorkerCreateView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("accounts/register/", WorkerCreateView.as_view(), name="worker-create"),
]

app_name = "core"
