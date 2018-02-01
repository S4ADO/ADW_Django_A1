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