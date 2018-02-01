from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as log_out
from .models import Task
from .forms import TaskCreateForm
from datetime import datetime

def home(request):
	if request.user.is_active == 0:
		return redirect('signin')
	return render(request, 'home.html', context = None)

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
			return render(request, 'home.html', context = None)
		else:
			error = form.errors
			return render(request, 'create.html', {'error' : error})	
	else:
		return render(request, 'create.html', context = None)

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

def logout(request):
	log_out(request)
	form = AuthenticationForm()
	return redirect('signin')

