from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import Worker


class WorkerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
        )


class WorkerNameSearch(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search"}
        )
    )


class TaskFiltersSearch(forms.Form):
    filters = forms.MultipleChoiceField(
        choices=[
            ("past_dl", "Past deadline❗"),
            ("done", "Done✅"),
            ("urgent", "Urgent⚡")
        ],
        label="",
        widget=forms.CheckboxSelectMultiple
    )
