from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, Task, Worker, Position, Project, Comment


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "project")

    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "project")}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "is_completed", "task_type", "project")


admin.site.register(TaskType)
admin.site.register(Position)
admin.site.register(Project)
admin.site.register(Comment)
