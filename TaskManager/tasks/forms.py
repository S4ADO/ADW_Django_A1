from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField
    date = forms.DateTimeField()

    class Meta:
        model = Task
        fields = ['title', 'body', 'date']

class TaskDeleteForm(forms.Form):
	taskid = forms.IntegerField()

class TaskEditForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField
    date = forms.DateTimeField()
    completed = forms.CharField(initial=True, required = False)
    id = forms.IntegerField()

    class Meta:
        model = Task
        fields = ['title', 'body', 'date', 'completed', 'id']	