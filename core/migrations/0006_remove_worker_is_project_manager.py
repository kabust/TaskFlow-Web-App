# Generated by Django 5.0.2 on 2024-03-05 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_project_project_manager_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="worker",
            name="is_project_manager",
        ),
    ]
