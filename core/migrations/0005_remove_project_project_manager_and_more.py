# Generated by Django 5.0.2 on 2024-03-05 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_task_project"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="project_manager",
        ),
        migrations.RemoveField(
            model_name="project",
            name="workers",
        ),
        migrations.AddField(
            model_name="worker",
            name="is_project_manager",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="worker",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.project",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                blank=True,
                default=1,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.project",
            ),
        ),
    ]