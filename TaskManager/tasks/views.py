from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as log_out
from .models import Task
from .forms import TaskCreateForm
from .forms import TaskEditForm
from .forms import TaskDeleteForm
from .forms import TaskSearchForm

#Display the home page once user has logged in
def home(request):
	if request.user.is_active == 0:
		return redirect('signin')
	tasks = Task.objects.filter(userid_id=request.user.id).order_by('-created_at')
	args = {'tasks': tasks}
	return render(request, 'home.html', args)

#Display the creation page and handle creation requests to insert into the database
def create(request):
	if request.user.is_active == 0:
		return redirect('signin')

	if request.method == 'POST':
		form = TaskCreateForm(data=request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.userid_id = request.user.id
			task.title = form.cleaned_data.get('title')
			task.bodym = form.cleaned_data.get('body')
			task.completed_at = form.cleaned_data.get('date')
			task.save()
			return redirect('home')
		else:
			error = form.errors
			return render(request, 'create.html', {'error' : error})
	else:
		return render(request, 'create.html', context = None)

#Search task bodies with given string
def search(request):
	if request.user.is_active == 0:
		return redirect('signin')

	if request.method == 'POST':
		form = TaskSearchForm(data=request.POST)
		if form.is_valid():
			search = form.cleaned_data.get('search')
			tasks = Task.objects.filter(body__contains=search,  userid_id = request.user.id)
			args = {'tasks': tasks, 'search' : search}
			return render(request, 'search.html', args)
		else:
			return render(request, 'home.html', context=None)
		
#Handle edits to task title, body, completion status and completion date and save to the database if exists
#Display the edit page when for a GET request
def edit(request, task_id):
	if request.user.is_active == 0:
		return redirect('signin')

	if request.method == 'POST':
		form = TaskEditForm(data=request.POST)
		if form.is_valid():
			count = Task.objects.filter(id = form.cleaned_data.get('id'), userid_id = request.user.id).count()
			if count == 1:
				task = Task.objects.get(id = form.cleaned_data.get('id'), userid_id = request.user.id)		
				task.title = form.cleaned_data.get('title')
				task.body = form.cleaned_data.get('body')
				task.completed_at = form.cleaned_data.get('date')
				if bool(form.cleaned_data.get('completed')):
					task.complete = 1
				else:
					task.complete = 0
				task.save()
				return redirect(home)
			else:
				return redirect('home')	
		else:
			return render(request, 'home.html', context=None)	

	elif request.method == "GET":
		count = Task.objects.filter(id = task_id, userid_id = request.user.id).count()
		if count == 1:
			task = Task.objects.get(id = task_id, userid_id = request.user.id)
			task.completed_at = str(task.completed_at)
			if "+" in task.completed_at:
				splitdate = task.completed_at.split("+")
				task.completed_at = splitdate[0]
			args = {'task': task}
			return render(request, 'edit.html', args)
		else:
			return render(request, 'home.html', context = None)	
	else:
		return render(request, 'home.html', context = None)	

#Delete tasks belonging to the user if exists
def delete(request):
	if request.user.is_active == 0:
		return redirect('signin')

	if request.method == 'POST':
		form = TaskDeleteForm(data=request.POST)
		if form.is_valid():
			count = Task.objects.filter(id = form.cleaned_data.get('taskid'), userid_id = request.user.id).count()
			if count == 1:
				task = Task.objects.filter(id = form.cleaned_data.get('taskid')).delete()
			return redirect('home')
		else:
			return render(request, 'home.html', context=None)	
	else:
		return render(request, 'home.html', context=None)	

#Register, uses built-in mehtods
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'register.html', {'form': form})

#Signin uses built-in methods
def signin(request):
	if request.user.is_active == 1:
		return redirect('home')
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active == 1:
					request.session.set_expiry(86400) #sets the exp. value of the session 
					login(request, user)
					return redirect('home')
	else:
		form = AuthenticationForm()
	return render(request, 'signin.html', {'form': form})	
	
#Log out uses built-in methods
def logout(request):
	log_out(request)
	form = AuthenticationForm()
	return redirect('signin')

