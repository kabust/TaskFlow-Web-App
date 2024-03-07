from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from core.models import Task, Project, Comment


class WorkerCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "project")


class WorkerUpdateForm(UserChangeForm):
    username = forms.CharField(max_length=255, disabled=True, required=False)
    date_joined = forms.DateTimeField(disabled=True, required=False)
    password = forms.CharField(
        disabled=True,
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "password",
        )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        users_project = self.request.user.project
        self.fields["assignees"].queryset = get_user_model().objects.filter(
            project=users_project
        )
        self.fields["assignees"].initial = self.instance
        self.fields["project"].required = True
        self.fields["project"].initial = Project.objects.get(worker=self.request.user)
        self.fields["project"].disabled = True

    class Meta:
        model = Task
        exclude = ("is_completed",)
        widgets = {"deadline": forms.widgets.DateInput(attrs={"type": "date"})}


class WorkerNameSearch(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )


class TaskFiltersSearch(forms.Form):
    filters = forms.MultipleChoiceField(
        choices=[
            ("past_dl", "Past deadline❗"),
            ("urgent", "Urgent⚡"),
            ("done", "Finished✅"),
        ],
        label="",
        widget=forms.CheckboxSelectMultiple,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content", "task", "commentator")
        widgets = {"task": forms.HiddenInput(), "commentator": forms.HiddenInput()}
